import random
import requests
import json
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from markitdown import MarkItDown

TAG = __name__
logger = setup_logging()

CHANNEL_MAP = {
    "V2EX": "v2ex-share",
    "Zhihu": "zhihu",
    "Weibo": "weibo",
    "Lianhe Zaobao": "zaobao",
    "cool": "coolapk",
    "MKTNews": "mktnews-flash",
    "Wall Street Insights": "wallstreetcn-quick",
    "36 krypton": "36kr-quick",
    "Tik Tok": "douyin",
    "Hupu": "hupu",
    "Baidu Tieba": "tieba",
    "Today's headlines": "toutiao",
    "IT Home": "ithome",
    "The Paper": "thepaper",
    "satellite news agency": "sputniknewscn",
    "Reference message": "cankaoxiaoxi",
    "Vision Forum": "pcbeta-windows11",
    "Financial Associated Press": "cls-depth",
    "snowball": "xueqiu-hotstock",
    "Gelonghui": "gelonghui",
    "Fab Finance": "fastbull-express",
    "Solidot": "solidot",
    "Hacker News": "hackernews",
    "Product Hunt": "producthunt",
    "Github": "github-trending-today",
    "Bilibili": "bilibili-hot-search",
    "quick worker": "kuaishou",
    "reliable news": "kaopu",
    "Golden Ten Data": "jin10",
    "Baidu hot search": "baidu",
    "Niuke": "nowcoder",
    "minority": "sspai",
    "Rare earth nuggets": "juejin",
    "ifeng.com": "ifeng",
    "Insect Tribe": "chongbuluo-latest",
}


# Default news source dictionary, used when not specified in the configuration
DEFAULT_NEWS_SOURCES = "The Paper; Baidu Hot Search; Financial Associated Press"


def get_news_sources_from_config(conn):
    """Get news source string from configuration"""
    try:
        # Try to get the news feed from the plugin configuration
        if (
            conn.config.get("plugins")
            and conn.config["plugins"].get("get_news_from_newsnow")
            and conn.config["plugins"]["get_news_from_newsnow"].get("news_sources")
        ):
            # Get the configured news source string
            news_sources_config = conn.config["plugins"]["get_news_from_newsnow"][
                "news_sources"
            ]

            if isinstance(news_sources_config, str) and news_sources_config.strip():
                logger.bind(tag=TAG).debug(f"Use configured news sources: {news_sources_config}")
                return news_sources_config
            else:
                logger.bind(tag=TAG).warning("The news source configuration is empty or has an incorrect format. Use the default configuration.")
        else:
            logger.bind(tag=TAG).debug("News source configuration not found, using default configuration")

        return DEFAULT_NEWS_SOURCES

    except Exception as e:
        logger.bind(tag=TAG).error(f"Failed to obtain news source configuration: {e}, use default configuration")
        return DEFAULT_NEWS_SOURCES


# Get all available news source names from CHANNEL_MAP
available_sources = list(CHANNEL_MAP.keys())
example_sources_str = "、".join(available_sources)

GET_NEWS_FROM_NEWSNOW_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_news_from_newsnow",
        "description": (
            "Get the latest news and randomly select a news item to broadcast."
            f"Users can choose different news sources, the standard name is: {example_sources_str}"
            "For example, when a user requests Baidu News, it is actually Baidu Hot Search. If not specified, it will be obtained from The Paper by default."
            "Users can request detailed content, and the detailed content of the news will be obtained."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "source": {
                    "type": "string",
                    "description": f"The standard Chinese name of the news source, such as {example_sources_str}, etc. Optional parameter, if not provided the default news source will be used",
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


def fetch_news_from_api(conn, source="thepaper"):
    """Get news list from API"""
    try:
        api_url = f"https://newsnow.busiyi.world/api/s?id={source}"
        if conn.config["plugins"].get("get_news_from_newsnow") and conn.config[
            "plugins"
        ]["get_news_from_newsnow"].get("url"):
            api_url = conn.config["plugins"]["get_news_from_newsnow"]["url"] + source

        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if "items" in data:
            return data["items"]
        else:
            logger.bind(tag=TAG).error(f"Get news API response format error: {data}")
            return []

    except Exception as e:
        logger.bind(tag=TAG).error(f"Failed to get news API: {e}")
        return []


def fetch_news_detail(url):
    """Get the content of the news details page and use MarkItDown to clean the HTML"""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Use MarkItDown to clean HTML content
        md = MarkItDown(enable_plugins=False)
        result = md.convert(response)

        # Get the cleaned text content
        clean_text = result.text_content

        # If the cleaned content is empty, a prompt message will be returned.
        if not clean_text or len(clean_text.strip()) == 0:
            logger.bind(tag=TAG).warning(f"The cleaned news content is empty: {url}")
            return "The news details cannot be parsed. It may be that the website has a special structure or the content is restricted."

        return clean_text
    except Exception as e:
        logger.bind(tag=TAG).error(f"Failed to get news details: {e}")
        return "Unable to get details"


@register_function(
    "get_news_from_newsnow",
    GET_NEWS_FROM_NEWSNOW_FUNCTION_DESC,
    ToolType.SYSTEM_CTL,
)
def get_news_from_newsnow(
    conn, source: str = "The Paper", detail: bool = False, lang: str = "zh_CN"
):
    """Get news and randomly select one to broadcast, or get the details of the previous news"""
    try:
        # Get the currently configured news source
        news_sources = get_news_sources_from_config(conn)

        # If detail is True, get the details of the previous news
        detail = str(detail).lower() == "true"
        if detail:
            if (
                not hasattr(conn, "last_newsnow_link")
                or not conn.last_newsnow_link
                or "url" not in conn.last_newsnow_link
            ):
                return ActionResponse(
                    Action.REQLLM,
                    "Sorry, the recently queried news was not found. Please get a piece of news first.",
                    None,
                )

            url = conn.last_newsnow_link.get("url")
            title = conn.last_newsnow_link.get("title", "Unknown title")
            source_id = conn.last_newsnow_link.get("source_id", "thepaper")
            source_name = CHANNEL_MAP.get(source_id, "unknown source")

            if not url or url == "#":
                return ActionResponse(
                    Action.REQLLM, "Sorry, there is no link available for this story for details.", None
                )

            logger.bind(tag=TAG).debug(
                f"Get news details: {title}, source: {source_name}, URL={url}"
            )

            # Get news details
            detail_content = fetch_news_detail(url)

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
                # f"News source: {source_name}\n"ame}\n"
                f"Detailed content: {detail_content}\n\n"
                f"(Please summarize the above news content, extract key information, and broadcast it to users in a natural and smooth way."
                f"Don’t mention that this is a summary, it’s like telling a complete news story)"
            )

            return ActionResponse(Action.REQLLM, detail_report, None)

        # Otherwise, get the news list and randomly select one
        # Convert Chinese name to English ID
        english_source_id = None

        # Check whether the entered Chinese name is in the configured news source
        news_sources_list = [
            name.strip() for name in news_sources.split(";") if name.strip()
        ]
        if source in news_sources_list:
            # If the entered Chinese name is in the configured news source, search the corresponding English ID in CHANNEL_MAP
            english_source_id = CHANNEL_MAP.get(source)

        # If the corresponding English ID cannot be found, use the default source
        if not english_source_id:
            logger.bind(tag=TAG).warning(f"Invalid news source: {source}, use the default source The Paper")
            english_source_id = "thepaper"
            source = "The Paper"

        logger.bind(tag=TAG).info(f"Get news: news source={source}({english_source_id})")

        # Get news list
        news_items = fetch_news_from_api(conn, english_source_id)

        if not news_items:
            return ActionResponse(
                Action.REQLLM,
                f"Sorry, unable to obtain news information from {source}, please try again later or try another news source.",
                None,
            )

        # Randomly select a piece of news
        selected_news = random.choice(news_items)

        # Save the current news link to the connection object for subsequent query details
        if not hasattr(conn, "last_newsnow_link"):
            conn.last_newsnow_link = {}
        conn.last_newsnow_link = {
            "url": selected_news.get("url", "#"),
            "title": selected_news.get("title", "Unknown title"),
            "source_id": english_source_id,
        }

        # Build a news report
        news_report = (
            f"Use {lang} to respond to the user's news query request based on the following data:\n\n"
            f"News title: {selected_news['title']}\n"
            # f"News source: {source}\n"rce}\n"
            f"(Please report this news headline to users in a natural and smooth way."
            f"Prompts the user to ask for detailed content, and the detailed content of the news will be obtained. )"
        )

        return ActionResponse(Action.REQLLM, news_report, None)

    except Exception as e:
        logger.bind(tag=TAG).error(f"Error getting news: {e}")
        return ActionResponse(
            Action.REQLLM, "Sorry, an error occurred while retrieving news, please try again later.", None
        )
