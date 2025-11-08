package xiaozhi.common.utils;

import org.apache.commons.lang3.StringUtils;

import jakarta.servlet.http.HttpServletRequest;
import lombok.extern.slf4j.Slf4j;

/*
*
*IP address
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
*/
@Slf4j
public class IpUtils {
    /*
*
     * get_ip_address
     * <p>
     * use_reverse_proxy_software_such_as_nginx， then_request_cannot_be_passed.getRemoteAddr()get_ip_address
* if_a_multilevel_reverse_proxy_is_used, X-Forwarded-For has more than one value, its_a_string_of_ip_addresses, the first non-unknown valid IP string in X-Forwarded-For, is_the_real_ip_address
*/
    public static String getIpAddr(HttpServletRequest request) {
        String unknown = "unknown";
        String ip = null;
        try {
            ip = request.getHeader("x-forwarded-for");
            if (StringUtils.isEmpty(ip) || unknown.equalsIgnoreCase(ip)) {
                ip = request.getHeader("Proxy-Client-IP");
            }
            if (StringUtils.isEmpty(ip) || ip.length() == 0 || unknown.equalsIgnoreCase(ip)) {
                ip = request.getHeader("WL-Proxy-Client-IP");
            }
            if (StringUtils.isEmpty(ip) || unknown.equalsIgnoreCase(ip)) {
                ip = request.getHeader("HTTP_CLIENT_IP");
            }
            if (StringUtils.isEmpty(ip) || unknown.equalsIgnoreCase(ip)) {
                ip = request.getHeader("HTTP_X_FORWARDED_FOR");
            }
            if (StringUtils.isEmpty(ip) || unknown.equalsIgnoreCase(ip)) {
                ip = request.getRemoteAddr();
            }
        } catch (Exception e) {
            log.error("IPUtils ERROR ", e);
        }

        return ip;
    }

}
