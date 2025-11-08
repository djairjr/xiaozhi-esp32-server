package xiaozhi.modules.timbre.vo;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * sound_details_display_vo
 * 
 * @author zjy
 * @since 2025-3-21
 */
@Data
public class TimbreDetailsVO implements Serializable {
    @Schema(description = "timbre id")
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

}
