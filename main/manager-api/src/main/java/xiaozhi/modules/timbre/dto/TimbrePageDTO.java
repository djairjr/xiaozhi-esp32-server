package xiaozhi.modules.timbre.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * tone_paging_parameter_dto
 * 
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Tone paging parameters")
public class TimbrePageDTO {

    @Schema(description = "Corresponds to TTS model primary key")
    @NotBlank(message = "{timbre.ttsModelId.require}")
    private String ttsModelId;

    @Schema(description = "Voice name")
    private String name;

    @Schema(description = "Number of pages")
    private String page;

    @Schema(description = "Display number of columns")
    private String limit;
}
