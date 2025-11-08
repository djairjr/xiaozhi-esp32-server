package xiaozhi.common.annotation;

import java.lang.annotation.Documented;
import java.lang.annotation.ElementType;
import java.lang.annotation.Retention;
import java.lang.annotation.RetentionPolicy;
import java.lang.annotation.Target;

/**
 * data_filtering_annotations
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface DataFilter {
    /**
     * table_alias
     */
    String tableAlias() default "";

    /**
     * user_id
     */
    String userId() default "creator";

    /**
     * department_id
     */
    String deptId() default "dept_id";

}