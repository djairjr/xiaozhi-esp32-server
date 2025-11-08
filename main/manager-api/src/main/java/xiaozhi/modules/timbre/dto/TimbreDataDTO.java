package xiaozhi.modules.timbre.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * tone_table_data_dto
 * 
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Tone table information")
public class TimbreDataDTO {

    @Schema(description = "language")
    @NotBlank(message = "{timbre.languages.require}")
    private String languages;

    @Schema(description = "Voice name")
    @NotBlank(message = "{timbre.name.require}")
    private String name;

    @Schema(description = "Remark")
    private String remark;

    @Schema(description = "Reference audio path")
    private String referenceAudio;

    @Schema(description = "Reference text")
    private String referenceText;

    @Schema(description = "sort")
    @Min(value = 0, message = "{sort.number}")
    private long sort;

    @Schema(description = "Corresponds to TTS model primary key")
    @NotBlank(message = "{timbre.ttsModelId.require}")
    private String ttsModelId;

    @Schema(description = "timbre encoding")
    @NotBlank(message = "{timbre.ttsVoice.require}")
    private String ttsVoice;

    @Schema(description = "Audio playback address")
    private String voiceDemo;
}