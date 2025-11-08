package xiaozhi.modules.security.entity;

import java.io.Serializable;
import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

/**
 * system_user_token
 */
@Data
@TableName("sys_user_token")
public class SysUserTokenEntity implements Serializable {

    /**
     * id
     */
    @TableId
    private Long id;
    /**
     * user_id
     */
    private Long userId;
    /**
     * user_token
     */
    private String token;
    /**
     * expiration_time
     */
    private Date expireDate;
    /**
     * update_time
     */
    private Date updateDate;
    /**
     * creation_time
     */
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;

}