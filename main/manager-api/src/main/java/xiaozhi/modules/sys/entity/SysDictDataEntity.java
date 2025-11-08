package xiaozhi.modules.sys.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;
import lombok.EqualsAndHashCode;
import xiaozhi.common.entity.BaseEntity;

/**
 * data_dictionary
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("sys_dict_data")
public class SysDictDataEntity extends BaseEntity {
    /**
     * dictionary_type_id
     */
    private Long dictTypeId;
    /**
     * dictionary_tag
     */
    private String dictLabel;
    /**
     * dictionary_value
     */
    private String dictValue;
    /**
     * remark
     */
    private String remark;
    /**
     * sort
     */
    private Integer sort;
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