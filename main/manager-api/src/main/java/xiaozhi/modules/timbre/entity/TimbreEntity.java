package xiaozhi.modules.timbre.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * tone_table_entity_class
 * 
 * @author zjy
 * @since 2025-3-21
 */
@Data
@EqualsAndHashCode(callSuper = false)
@TableName("ai_tts_voice")
@Schema(description = "timbre information")
public class TimbreEntity {

    @Schema(description = "id")
    private String id;

    @Schema(description = "language")
    private String languages;

    @Schema(description = "Voice name")
    private String name;

    @Schema(description = "Remark")
    private String remark;

    @Schema(description = "Reference audio path")
    private String referenceAudio;

    @Schema(description = "Reference text")
    private String referenceText;

    @Schema(description = "sort")
    private long sort;

    @Schema(description = "Corresponds to TTS model primary key")
    private String ttsModelId;

    @Schema(description = "timbre encoding")
    private String ttsVoice;

    @Schema(description = "Audio playback address")
    private String voiceDemo;

    @Schema(description = "Updater")
    @TableField(fill = FieldFill.UPDATE)
    private Long updater;

    @Schema(description = "Update time")
    @TableField(fill = FieldFill.UPDATE)
    private Date updateDate;

    @Schema(description = "Creator")
    @TableField(fill = FieldFill.INSERT)
    private Long creator;

    @Schema(description = "creation time")
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;

}