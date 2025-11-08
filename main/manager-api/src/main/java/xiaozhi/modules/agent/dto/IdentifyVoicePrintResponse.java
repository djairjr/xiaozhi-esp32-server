package xiaozhi.modules.agent.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

import lombok.Data;

/**
 * the_object_returned_by_the_voiceprint_recognition_interface
 */
@Data
public class IdentifyVoicePrintResponse {
    /**
     * best_matching_voiceprint_id
     */
    @JsonProperty("speaker_id")
    private String speakerId;
    /**
     * voiceprint_score
     */
    private Double score;
}
