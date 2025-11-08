import random
import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action

TAG = __name__
logger = setup_logging()

GET_NEWS_FROM_CHINANEWS_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_news_from_chinanews",
        "description": (
            "Get the latest news and randomly select a news item to broadcast."
            "Users can specify news types, such as social news, technology news, international news, etc."
            "If not specified, social news will be broadcast by default."
            "Users can request detailed content, and the detailed content of the news will be obtained."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "category": {
                    "type": "string",
                    "description": "News categories such as Society, Technology, International. Optional parameter, if not provided the default category is used",
                },
                "detail": {
                    "type": "boolean",
                    "description": "Whether to obtain detailed content, the default is false. If true, get the details of the previous news",
                },
                "lang": {
                    "type": "string",
                    "description": "Returns the language code used by the user, such as zh_CN/zh_HK/en_US/ja_JP, etc., the default is zh_CN",
                },
            },
            "required": ["lang"],
        },
    },
}


def fetch_news_from_rss(rss_url):
    """Get news list from RSS feed"""
    try:
        response = requests.get(rss_url)
        response.raise_for_status()

        # Parse XML
        root = ET.fromstring(response.content)

        # Find all item elements (news items)
        news_items = []
        for item in root.findall(".//item"):
            title = (
                item.find("title").text if item.find("title") is not None else "Untitled"
            )
            link = item.find("link").text if item.find("link") is not None else "#"
            description = (
                item.find("description").text
                if item.find("description") is not None
                else "No description"
            )
            pubDate = (
                item.find("pubDate").text
                if item.find("pubDate") is not None
                else "unknown time"
            )

            news_items.append(
                {
                    "title": title,
                    "link": link,
                    "description": description,
                    "pubDate": pubDate,
                }
            )

        return news_items
    except Exception as e:
        logger.bind(tag=TAG).error(f"Failed to get RSS news: {e}")
        return []


def fetch_news_detail(url):
    """Get the content of the news details page and summarize it"""
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        # Try to extract the body content (the selector here needs to be adjusted according to the actual website structure)
        content_div = soup.select_one(
            ".content_desc, .content, article, .article-content"
        )
        if content_div:
            paragraphs = content_div.find_all("p")
            content = "\n".join(
                [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            )
            return content
        else:
            # If a specific content area is not found, try to get all paragraphs
            paragraphs = soup.find_all("p")
            content = "\n".join(
                [p.get_text().strip() for p in paragraphs if p.get_text().strip()]
            )
            return content[:2000]  # Limit length
    except Exception as e:
        logger.bind(tag=TAG).error(f"Failed to get news details: {e}")
        return "Unable to get details"


def map_category(category_text):
    """Map user-entered Chinese categories to category keys in the configuration file"""
    if not category_text:
        return None

    # Category mapping dictionary, currently supports social, international, and financial news. For more types, see the configuration file
    category_map = {
        # social news
        "society": "society_rss_url",
        "social news": "society_rss_url",
        # international news
        "internationality": "world_rss_url",
        "international news": "world_rss_url",
        # financial news
        "Finance": "finance_rss_url",
        "financial news": "finance_rss_url",
        "finance": "finance_rss_url",
        "economy": "finance_rss_url",
    }

    # Convert to lowercase and remove spaces
    normalized_category = category_text.lower().strip()

    # Returns the mapping result, or the original input if there is no match
    return category_map.get(normalized_category, category_text)


@register_function(
    "get_news_from_chinanews",
    GET_NEWS_FROM_CHINANEWS_FUNCTION_DESC,
    ToolType.SYSTEM_CTL,
)
def get_news_from_chinanews(
    conn, category: str = None, detail: bool = False, lang: str = "zh_CN"
):
    """Get news and randomly select one to broadcast, or get the details of the previous news"""
    try:
        # If detail is True, get the details of the previous news
        if detail:
            if (
                not hasattr(conn, "last_news_link")
                or not conn.last_news_link
                or "link" not in conn.last_news_link
            ):
                return ActionResponse(
                    Action.REQLLM,
                    "Sorry, the recently queried news was not found. Please get a piece of news first.",
                    None,
                )

            link = conn.last_news_link.get("link")
            title = conn.last_news_link.get("title", "Unknown title")

            if link == "#":
                return ActionResponse(
                    Action.REQLLM, "Sorry, there is no link available for this story for details.", None
                )

            logger.bind(tag=TAG).debug(f"Get news details: {title}, URL={link}")

            # Get news details
            detail_content = fetch_news_detail(link)

            if not detail_content or detail_content == "Unable to get details":
                return ActionResponse(
                    Action.REQLLM,
                    f"Sorry, the detailed content of "{title}" cannot be obtained. It may be that the link has expired or the website structure has changed.",
                    None,
                )

            # Build details report
            detail_report = (
                f"Use {lang} to respond to the user's news details query request based on the following data:\n\n"
                f"News title: {title}\n"
                f"Detailed content: {detail_content}\n\n"
                f"(Please summarize the above news content, extract key information, and broadcast it to users in a natural and smooth way."
                f"Don’t mention that this is a summary, it’s like telling a complete news story)"
            )

            return ActionResponse(Action.REQLLM, detail_report, None)

        # Otherwise, get the news list and randomly select one
        # Get RSS URL from configuration
        rss_config = conn.config["plugins"]["get_news_from_chinanews"]
        default_rss_url = rss_config.get(
            "default_rss_url", "https://www.chinanews.com.cn/rss/society.xml"
        )

        # Map user-entered categories to category keys in the configuration
        mapped_category = map_category(category)

        # If a category is provided, try to get the corresponding URL from the configuration
        rss_url = default_rss_url
        if mapped_category and mapped_category in rss_config:
            rss_url = rss_config[mapped_category]

        logger.bind(tag=TAG).info(
            f"Get news: original category={category}, mapped category={mapped_category}, URL={rss_url}"
        )

        # Get news list
        news_items = fetch_news_from_rss(rss_url)

        if not news_items:
            return ActionResponse(
                Action.REQLLM, "Sorry, failed to obtain news information, please try again later.", None
            )

        # Randomly select a piece of news
        selected_news = random.choice(news_items)

        # Save the current news link to the connection object for subsequent query details
        if not hasattr(conn, "last_news_link"):
            conn.last_news_link = {}
        conn.last_news_link = {
            "link": selected_news.get("link", "#"),
            "title": selected_news.get("title", "Unknown title"),
        }

        # Build a news report
        news_report = (
            f"Use {lang} to respond to the user's news query request based on the following data:\n\n"
            f"News title: {selected_news['title']}\n"
            f"Release time: {selected_news['pubDate']}\n"
            f"News content: {selected_news['description']}\n"
            f"(Please report this news to users in a natural and smooth way, and summarize the content appropriately."
            f"Just read the news directly without any extra content."
            f"If the user asks for more details, inform the user that they can say 'please tell me more about this news' to get more content)"
        )

        return ActionResponse(Action.REQLLM, news_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"Error getting news: {e}")
        return ActionResponse(
            Action.REQLLM, "Sorry, an error occurred while retrieving news, please try again later.", None
        )
