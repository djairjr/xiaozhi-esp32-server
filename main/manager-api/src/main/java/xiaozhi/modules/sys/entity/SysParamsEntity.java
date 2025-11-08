package xiaozhi.modules.sys.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;
import lombok.EqualsAndHashCode;
import xiaozhi.common.entity.BaseEntity;

/**
 * parameter_management
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("sys_params")
public class SysParamsEntity extends BaseEntity {
    /**
     * parameter_encoding
     */
    private String paramCode;
    /**
     * parameter_value
     */
    private String paramValue;
    /**
     * value_type：string-string，number-number，boolean-boolean，array-array
     */
    private String valueType;
    /**
     * type 0：system_parameters 1：nonsystem_parameters
     */
    private Integer paramType;
    /**
     * remark
     */
    private String remark;
    /**
     * updater
     */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Long updater;
    /**
     * update_time
     */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Date updateDate;

}