package xiaozhi.common.entity;

import java.io.Serializable;
import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;

import lombok.Data;

/**
 * basic_entity_class，all_entities_need_to_inherit
 * Copyright (c) open_source_for_everyone All rights reserved.
 * Website: https://www.renren.io
 */
@Data
public abstract class BaseEntity implements Serializable {
    /**
     * id
     */
    @TableId
    private Long id;
    /**
     * creator
     */
    @TableField(fill = FieldFill.INSERT)
    private Long creator;
    /**
     * creation_time
     */
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;
}