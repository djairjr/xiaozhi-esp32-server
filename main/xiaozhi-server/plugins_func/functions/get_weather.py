import requests
from bs4 import BeautifulSoup
from config.logger import setup_logging
from plugins_func.register import register_function, ToolType, ActionResponse, Action
from core.utils.util import get_ip_info

TAG = __name__
logger = setup_logging()

GET_WEATHER_FUNCTION_DESC = {
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": (
            "To get the weather of a certain place, the user should provide a location. For example, if the user says the weather in Hangzhou, the parameter is: Hangzhou."
            "If the user refers to a province, the provincial capital city is used by default. If the user refers to a place name instead of a province or city, the capital city of the province where the place is located will be used by default."
            "If the user does not specify a location and says "What's the weather like" or "What's the weather like today", the location parameter is empty."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Place name, such as Hangzhou. Optional parameter, if not provided, it will not be passed",
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

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
    )
}

# Weather code https://dev.qweather.com/docs/resource/icons/#weather-icons
WEATHER_CODE_MAP = {
    "100": "clear",
    "101": "partly cloudy",
    "102": "Shaoyun",
    "103": "Partly cloudy",
    "104": "Negative",
    "150": "clear",
    "151": "partly cloudy",
    "152": "Shaoyun",
    "153": "Partly cloudy",
    "300": "shower",
    "301": "strong showers",
    "302": "thundershowers",
    "303": "Severe thundershowers",
    "304": "Thundershowers with hail",
    "305": "light rain",
    "306": "Moderate rain",
    "307": "heavy rain",
    "308": "extreme rainfall",
    "309": "drizzle/drizzle",
    "310": "rainstorm",
    "311": "Heavy rain",
    "312": "Extremely heavy rain",
    "313": "freezing rain",
    "314": "light to moderate rain",
    "315": "moderate to heavy rain",
    "316": "Heavy rain",
    "317": "Heavy rain to heavy rain",
    "318": "Heavy rain to extremely heavy rain",
    "350": "shower",
    "351": "strong showers",
    "399": "rain",
    "400": "Xiaoxue",
    "401": "Moderate snow",
    "402": "heavy snow",
    "403": "blizzard",
    "404": "sleet",
    "405": "Rain and snow weather",
    "406": "Showers of sleet",
    "407": "snow showers",
    "408": "light to moderate snow",
    "409": "Moderate to heavy snow",
    "410": "As big as a blizzard",
    "456": "Showers of sleet",
    "457": "snow showers",
    "499": "Snow",
    "500": "mist",
    "501": "fog",
    "502": "haze",
    "503": "blowing sand",
    "504": "floating dust",
    "507": "sandstorm",
    "508": "Strong sandstorm",
    "509": "Dense fog",
    "510": "Strong dense fog",
    "511": "moderate haze",
    "512": "severe haze",
    "513": "severe haze",
    "514": "Heavy fog",
    "515": "Extremely dense fog",
    "900": "hot",
    "901": "cold",
    "999": "unknown",
}


def fetch_city_info(location, api_key, api_host):
    url = f"https://{api_host}/geo/v2/city/lookup?key={api_key}&location={location}&lang=zh"
    response = requests.get(url, headers=HEADERS).json()
    if response.get("error") is not None:
        logger.bind(tag=TAG).error(
            f"Failed to get weather, reason: {response.get('error', {}).get('detail')}"
        )
        return None
    return response.get("location", [])[0] if response.get("location") else None


def fetch_weather_page(url):
    response = requests.get(url, headers=HEADERS)
    return BeautifulSoup(response.text, "html.parser") if response.ok else None


def parse_weather_info(soup):
    city_name = soup.select_one("h1.c-submenu__location").get_text(strip=True)

    current_abstract = soup.select_one(".c-city-weather-current .current-abstract")
    current_abstract = (
        current_abstract.get_text(strip=True) if current_abstract else "unknown"
    )

    current_basic = {}
    for item in soup.select(
        ".c-city-weather-current .current-basic .current-basic___item"
    ):
        parts = item.get_text(strip=True, separator=" ").split(" ")
        if len(parts) == 2:
            key, value = parts[1], parts[0]
            current_basic[key] = value

    temps_list = []
    for row in soup.select(".city-forecast-tabs__row")[:7]:  # Get the data of the previous 7 days
        date = row.select_one(".date-bg .date").get_text(strip=True)
        weather_code = (
            row.select_one(".date-bg .icon")["src"].split("/")[-1].split(".")[0]
        )
        weather = WEATHER_CODE_MAP.get(weather_code, "unknown")
        temps = [span.get_text(strip=True) for span in row.select(".tmp-cont .temp")]
        high_temp, low_temp = (temps[0], temps[-1]) if len(temps) >= 2 else (None, None)
        temps_list.append((date, weather, high_temp, low_temp))

    return city_name, current_abstract, current_basic, temps_list


@register_function("get_weather", GET_WEATHER_FUNCTION_DESC, ToolType.SYSTEM_CTL)
def get_weather(conn, location: str = None, lang: str = "zh_CN"):
    from core.utils.cache.manager import cache_manager, CacheType

    api_host = conn.config["plugins"]["get_weather"].get(
        "api_host", "mj7p3y7naa.re.qweatherapi.com"
    )
    api_key = conn.config["plugins"]["get_weather"].get(
        "api_key", "a861d0d5e7bf4ee1a83d9a9e4f96d4da"
    )
    default_location = conn.config["plugins"]["get_weather"]["default_location"]
    client_ip = conn.client_ip

    # Prioritize using location parameters provided by the user
    if not location:
        # Parse city by client IP
        if client_ip:
            # First obtain the city information corresponding to the IP from the cache
            cached_ip_info = cache_manager.get(CacheType.IP_INFO, client_ip)
            if cached_ip_info:
                location = cached_ip_info.get("city")
            else:
                # Cache miss, call API to obtain
                ip_info = get_ip_info(client_ip, logger)
                if ip_info:
                    cache_manager.set(CacheType.IP_INFO, client_ip, ip_info)
                    location = ip_info.get("city")

            if not location:
                location = default_location
        else:
            # If there is no IP, use the default location
            location = default_location
    # Try to get the full weather report from cache
    weather_cache_key = f"full_weather_{location}_{lang}"
    cached_weather_report = cache_manager.get(CacheType.WEATHER, weather_cache_key)
    if cached_weather_report:
        return ActionResponse(Action.REQLLM, cached_weather_report, None)

    # Cache miss, getting real-time weather data
    city_info = fetch_city_info(location, api_key, api_host)
    if not city_info:
        return ActionResponse(
            Action.REQLLM, f"No relevant city found: {location}, please confirm whether the location is correct", None
        )
    soup = fetch_weather_page(city_info["fxLink"])
    if not soup:
        return ActionResponse(Action.REQLLM, None, "Request failed")
    city_name, current_abstract, current_basic, temps_list = parse_weather_info(soup)

    weather_report = f"The location you are querying is: {city_name}\n\nCurrent weather: {current_abstract}\n"

    # Add valid current weather parameters
    if current_basic:
        weather_report += "Detailed parameters:\n"
        for key, value in current_basic.items():
            if value != "0":  # Filter invalid values
                weather_report += f"  · {key}: {value}\n"

    # Add 7-day forecast
    weather_report += "\nForecast for the next 7 days:\n"
    for date, weather, high, low in temps_list:
        weather_report += f"{date}: {weather}, temperature {low}~{high}\n"

    # prompt
    weather_report += "\n(If you need the specific weather on a certain day, please tell me the date)"

    # Caching full weather reports
    cache_manager.set(CacheType.WEATHER, weather_cache_key, weather_report)

    return ActionResponse(Action.REQLLM, weather_report, None)
