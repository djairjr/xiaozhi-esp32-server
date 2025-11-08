package xiaozhi.common.xss;

import java.util.Collections;
import java.util.List;

import org.springframework.boot.context.properties.ConfigurationProperties;

import lombok.Data;

/**
 * XSS configuration_items
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
@Data
@ConfigurationProperties(prefix = "renren.xss")
public class XssProperties {
    /**
     * whether_to_enable XSS
     */
    private boolean enabled;
    /**
     * excluded_url_list
     */
    private List<String> excludeUrls = Collections.emptyList();
}
