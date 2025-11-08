package xiaozhi.modules.voiceclone.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

@Data
@EqualsAndHashCode(callSuper = false)
@TableName("ai_voice_clone")
@Schema(description = "sound cloning")
public class VoiceCloneEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "unique identifier")
    private String id;

    @Schema(description = "sound name")
    private String name;

    @Schema(description = "model id")
    private String modelId;

    @Schema(description = "sound id")
    private String voiceId;

    @Schema(description = "User ID (associated user table)")
    private Long userId;

    @Schema(description = "sound")
    private byte[] voice;

    @Schema(description = "Training status: 0 pending training 1 training 2 training successful 3 training failed")
    private Integer trainStatus;

    @Schema(description = "Reasons for training errors")
    private String trainError;

    @Schema(description = "Creator")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "creation time")
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;
}
