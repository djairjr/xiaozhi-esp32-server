package xiaozhi.modules.agent.dto;

import java.io.Serializable;
import java.util.HashMap;
import java.util.List;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/*
*
 * agent_update_dto
* dedicated_to_updating_agents, id field is required, used_to_identify_the_agent_to_be_updated
 * all_other_fields_are_optional，only_update_provided_fields
*/
@Data
@Schema(description = "Agent update object")
public class AgentUpdateDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "agent coding", example = "AGT_1234567890", nullable = true)
    private String agentCode;

    @Schema(description = "Agent name", example = "Customer service assistant", nullable = true)
    private String agentName;

    @Schema(description = "Speech recognition model identification", example = "asr_model_02", nullable = true)
    private String asrModelId;

    @Schema(description = "Voice activity detection logo", example = "vad_model_02", nullable = true)
    private String vadModelId;

    @Schema(description = "Large language model identifier", example = "llm_model_02", nullable = true)
    private String llmModelId;

    @Schema(description = "VLLM model identification", example = "vllm_model_02", required = false)
    private String vllmModelId;

    @Schema(description = "Speech synthesis model identification", example = "tts_model_02", required = false)
    private String ttsModelId;

    @Schema(description = "timbre identity", example = "voice_02", nullable = true)
    private String ttsVoiceId;

    @Schema(description = "memory model identifier", example = "mem_model_02", nullable = true)
    private String memModelId;

    @Schema(description = "Intent model identifier", example = "intent_model_02", nullable = true)
    private String intentModelId;

    @Schema(description = "Plug-in function information", nullable = true)
    private List<FunctionInfo> functions;

    @Schema(description = "Character setting parameters", example = "You are a professional customer service assistant responsible for answering user questions and providing assistance", nullable = true)
    private String systemPrompt;

    @Schema(description = "Summary memory", example = "Build a growable dynamic memory network, retain_critical_information_in_a_limited_space, evolution_track_of_intelligent_maintenance_information\n"
            + "Summarize_important_information_about_the_user based on conversation history to provide more personalized service in future conversations", nullable = true)
    private String summaryMemory;

    @Schema(description = "Chat record configuration (0 does not record, 1 records text only, 2 records text and voice)", example = "3", nullable = true)
    private Integer chatHistoryConf;

    @Schema(description = "language encoding", example = "zh_CN", nullable = true)
    private String langCode;

    @Schema(description = "interactive language", example = "Chinese", nullable = true)
    private String language;

    @Schema(description = "sort", example = "1", nullable = true)
    private Integer sort;

    @Data
    @Schema(description = "Plug-in function information")
    public static class FunctionInfo implements Serializable {
        @Schema(description = "Plugin ID", example = "plugin_01")
        private String pluginId;

        @Schema(description = "Function parameter information", nullable = true)
        private HashMap<String, Object> paramInfo;

        private static final long serialVersionUID = 1L;
    }
}