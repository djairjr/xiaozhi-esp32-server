package xiaozhi.modules.voiceclone.dto;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * sound_clone_response_dto
 * used_to_display_sound_clone_information_to_the_front_end，contains_model_name_and_user_name
 */
@Data
@Schema(description = "Sound clone response DTO")
public class VoiceCloneResponseDTO {

    @Schema(description = "unique identifier")
    private String id;

    @Schema(description = "sound name")
    private String name;

    @Schema(description = "model id")
    private String modelId;

    @Schema(description = "Model name")
    private String modelName;

    @Schema(description = "sound id")
    private String voiceId;

    @Schema(description = "User ID (associated user table)")
    private Long userId;

    @Schema(description = "Username")
    private String userName;

    @Schema(description = "Training status: 0 pending training 1 training 2 training successful 3 training failed")
    private Integer trainStatus;

    @Schema(description = "Reasons for training errors")
    private String trainError;

    @Schema(description = "creation time")
    private Date createDate;

    @Schema(description = "Is there audio data?")
    private Boolean hasVoice;
}