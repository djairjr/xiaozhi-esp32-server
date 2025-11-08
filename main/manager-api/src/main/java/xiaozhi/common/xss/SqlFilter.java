package xiaozhi.common.xss;

import org.apache.commons.lang3.StringUtils;

import xiaozhi.common.exception.ErrorCode;
import xiaozhi.common.exception.RenException;

/*
*
* SQL filtering
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
*/
public class SqlFilter {

    /*
*
* SQL injection filtering
     *
     * @param str string_to_be_verified
*/
    public static String sqlInject(String str) {
        if (StringUtils.isBlank(str)) {
            return null;
        }
        // Remove '|"|;|\character
        str = StringUtils.replace(str, "'", "");
        str = StringUtils.replace(str, "\"", "");
        str = StringUtils.replace(str, ";", "");
        str = StringUtils.replace(str, "\\", "");

        // convert_to_lowercase
        str = str.toLowerCase();

        // illegal_characters
        String[] keywords = { "master", "truncate", "insert", "select", "delete", "update", "declare", "alter",
                "drop" };

        // determine_whether_it_contains_illegal_characters
        for (String keyword : keywords) {
            if (str.contains(keyword)) {
                throw new RenException(ErrorCode.INVALID_SYMBOL);
            }
        }

        return str;
    }
}
