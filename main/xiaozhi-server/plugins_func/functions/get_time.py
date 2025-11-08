from datetime import datetime
import cnlunar
from plugins_func.register import register_function, ToolType, ActionResponse, Action

get_lunar_function_desc = {
    "type": "function",
    "function": {
        "name": "get_lunar",
        "description": (
            "Lunar/lunar and almanac information for specific dates."
            "Users can specify the query content, such as: lunar calendar date, celestial stems and earthly branches, solar terms, zodiac signs, constellations, horoscopes, taboos, etc."
            "If no query content is specified, the zodiac year and lunar date will be queried by default."
            "For basic queries such as 'Today's lunar calendar date' and 'Today's lunar calendar date', please use the information in the context directly and do not call this tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "The date to be queried is in the format YYYY-MM-DD, for example, 2024-01-01. If not provided, the current date is used",
                },
                "query": {
                    "type": "string",
                    "description": "Content to be queried, such as lunar calendar dates, zodiac signs, festivals, solar terms, zodiac signs, constellations, horoscopes, taboos, etc.",
                },
            },
            "required": [],
        },
    },
}


@register_function("get_lunar", get_lunar_function_desc, ToolType.WAIT)
def get_lunar(date=None, query=None):
    """Used to obtain the current lunar/lunar calendar, and almanac information such as celestial stems and earthly branches, solar terms, zodiac signs, constellations, horoscopes, taboos, etc."""
    from core.utils.cache.manager import cache_manager, CacheType

    # If a date argument is provided, the specified date is used; otherwise the current date is used
    if date:
        try:
            now = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            return ActionResponse(
                Action.REQLLM,
                f"The date format is wrong, please use YYYY-MM-DD format, for example: 2024-01-01",
                None,
            )
    else:
        now = datetime.now()

    current_date = now.strftime("%Y-%m-%d")

    # If query is None, the default text is used
    if query is None:
        query = "By default, the zodiac year and lunar date are queried"

    # Try to get lunar calendar information from cache
    lunar_cache_key = f"lunar_info_{current_date}"
    cached_lunar_info = cache_manager.get(CacheType.LUNAR, lunar_cache_key)
    if cached_lunar_info:
        return ActionResponse(Action.REQLLM, cached_lunar_info, None)

    response_text = f"Respond to the user's query request and provide information related to {query} based on the following information:\n"

    lunar = cnlunar.Lunar(now, godType="8char")
    response_text += (
        "Lunar calendar information:\n"
        "%syear%s%s\n" % (lunar.lunarYearCn, lunar.lunarMonthCn[:-1], lunar.lunarDayCn)
        + "Stems and branches: %s year %s month %s day\n" % (lunar.year8Char, lunar.month8Char, lunar.day8Char)
        + "Zodiac: Genus %s\n" % (lunar.chineseYearZodiac)
        + "BaZi: %s\n"
        % (
            " ".join(
                [lunar.year8Char, lunar.month8Char, lunar.day8Char, lunar.twohour8Char]
            )
        )
        + "Today's holiday: %s\n"
        % (
            ",".join(
                filter(
                    None,
                    (
                        lunar.get_legalHolidays(),
                        lunar.get_otherHolidays(),
                        lunar.get_otherLunarHolidays(),
                    ),
                )
            )
        )
        + "Today's solar term: %s\n" % (lunar.todaySolarTerms)
        + "Next solar term: %s %s year %s month %s day\n"
        % (
            lunar.nextSolarTerm,
            lunar.nextSolarTermYear,
            lunar.nextSolarTermDate[0],
            lunar.nextSolarTermDate[1],
        )
        + "This year’s solar terms table: %s\n"
        % (
            ", ".join(
                [
                    f"{term}({date[0]} month {date[1]} day)"
                    for term, date in lunar.thisYearSolarTermsDic.items()
                ]
            )
        )
        + "Zodiac sign: %s\n" % (lunar.chineseZodiacClash)
        + "Zodiac sign: %s\n" % (lunar.starZodiac)
        + "Nayin: %s\n" % lunar.get_nayin()
        + "Peng Zubaiji: %s\n" % (lunar.get_pengTaboo(delimit=", "))
        + "Duty: %s is on duty\n" % lunar.get_today12DayOfficer()[0]
        + "Value: %s(%s)\n"
        % (lunar.get_today12DayOfficer()[1], lunar.get_today12DayOfficer()[2])
        + "Nirvana: %s\n" % lunar.get_the28Stars()
        + "Lucky direction: %s\n" % " ".join(lunar.get_luckyGodsDirection())
        + "Today’s Fetus God: %s\n" % lunar.get_fetalGod()
        + "Appropriate: %s\n" % "、".join(lunar.goodThing[:10])
        + "Taboo: %s\n" % "、".join(lunar.badThing[:10])
        + "(The year of the zodiac and the lunar calendar date are returned by default; today's taboos are only returned when requesting to query taboo information)"
    )

    # Caching lunar calendar information
    cache_manager.set(CacheType.LUNAR, lunar_cache_key, response_text)

    return ActionResponse(Action.REQLLM, response_text, None)
