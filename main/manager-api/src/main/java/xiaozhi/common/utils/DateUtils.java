package xiaozhi.common.utils;

import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.temporal.ChronoUnit;
import java.util.Date;

/**
 * date_processing
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
public class DateUtils {
    /**
     * time_format(yyyy-MM-dd)
     */
    public final static String DATE_PATTERN = "yyyy-MM-dd";
    /**
     * time_format(yyyy-MM-dd HH:mm:ss)
     */
    public final static String DATE_TIME_PATTERN = "yyyy-MM-dd HH:mm:ss";
    public final static String DATE_TIME_MILLIS_PATTERN = "yyyy-MM-dd HH:mm:ss.SSS";


    /*
*
     * date_formatting the_date_format_is：yyyy-MM-dd
     *
     * @param date date
* @return returnyyyy-MM-dd format date
*/
    public static String format(Date date) {
        return format(date, DATE_PATTERN);
    }

    /*
*
     * date_formatting the_date_format_is：yyyy-MM-dd
     *
     * @param date    date
     * @param pattern format，like：DateUtils.DATE_TIME_PATTERN
* @return returnyyyy-MM-dd format date
*/
    public static String format(Date date, String pattern) {
        if (date != null) {
            SimpleDateFormat df = new SimpleDateFormat(pattern);
            return df.format(date);
        }
        return null;
    }

    /**
     * date_parsing
     *
     * @param date    date
     * @param pattern format，like：DateUtils.DATE_TIME_PATTERN
     * @return return_date
     */
    public static Date parse(String date, String pattern) {
        try {
            return new SimpleDateFormat(pattern).parse(date);
        } catch (ParseException e) {
            e.printStackTrace();
        }
        return null;
    }


    public static String getDateTimeNow() {
        return getDateTimeNow(DATE_TIME_PATTERN);
    }

    public static String getDateTimeNow(String pattern) {
        return format(new Date(), pattern);
    }

    public static String millsToSecond(long mills) {
        return String.format("%.3f", mills / 1000.0);
    }

    /*
*
* get_a_short_time_string: returns just 10 seconds ago, how_many_seconds_ago, hours_ago, returns_year_month_day_hour_minute_and_second_if_more_than_one_week_has_passed
     * @param date
     * @return
*/
    public static String getShortTime(Date date) {
        if (date == null) {
            return null;
        }
        // will Date convert_to Instant
        LocalDateTime localDateTime = date.toInstant()
                // get_the_system_default_time_zone
                .atZone(ZoneId.systemDefault())
                // convert_to LocalDateTime
                .toLocalDateTime();
        // current_time
        LocalDateTime now = LocalDateTime.now();
        // time_difference，unit_is_seconds
        long secondsBetween = ChronoUnit.SECONDS.between(localDateTime, now);

        if (secondsBetween <= 10) {
            return "just";
        } else if (secondsBetween < 60) {
            return secondsBetween + "seconds ago";
        } else if (secondsBetween < 60 * 60) {
            return secondsBetween / 60 + "minutes ago";
        } else if (secondsBetween < 86400) {
            return secondsBetween / 3600 + "hours ago";
        } else if (secondsBetween < 604800) {
            return secondsBetween / 86400 + "days ago";
        } else {
            // more_than_a_week，show_full_date_time
            return format(date,DATE_TIME_PATTERN);
        }
    }
}
