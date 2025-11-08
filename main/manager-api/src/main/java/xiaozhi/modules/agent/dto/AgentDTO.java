package xiaozhi.modules.agent.dto;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * agent_data_transfer_object
 * used_to_transfer_agentrelated_data_between_the_service_layer_and_the_controller_layer
 */
@Data
@Schema(description = "agent object")
public class AgentDTO {
    @Schema(description = "agent coding", example = "AGT_1234567890")
    private String id;

    @Schema(description = "Agent name", example = "Customer service assistant")
    private String agentName;

    @Schema(description = "Speech synthesis model name", example = "tts_model_01")
    private String ttsModelName;

    @Schema(description = "Voice name", example = "voice_01")
    private String ttsVoiceName;

    @Schema(description = "Large language model name", example = "llm_model_01")
    private String llmModelName;

    @Schema(description = "Visual model name", example = "vllm_model_01")
    private String vllmModelName;

    @Schema(description = "Memory model ID", example = "mem_model_01")
    private String memModelId;

    @Schema(description = "Character setting parameters", example = "You are a professional customer service assistant responsible for answering user questions and providing assistance")
    private String systemPrompt;

    @Schema(description = "Summary memory", example = "Build a growable dynamic memory network, retain_critical_information_in_a_limited_space, evolution_track_of_intelligent_maintenance_information\n" +
            "Summarize_important_information_about_the_user based on conversation history to provide more personalized service in future conversations", required = false)
    private String summaryMemory;

    @Schema(description = "Last connection time", example = "2024-03-20 10:00:00")
    private Date lastConnectedAt;

    @Schema(description = "Number of devices", example = "10")
    private Integer deviceCount;
}