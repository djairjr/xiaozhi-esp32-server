package xiaozhi.modules.agent.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@TableName("ai_agent")
@Schema(description = "Agent information")
public class AgentEntity {

    @TableId(type = IdType.ASSIGN_UUID)
    @Schema(description = "Agent unique identifier")
    private String id;

    @Schema(description = "Belonging user ID")
    private Long userId;

    @Schema(description = "agent coding")
    private String agentCode;

    @Schema(description = "Agent name")
    private String agentName;

    @Schema(description = "Speech recognition model identification")
    private String asrModelId;

    @Schema(description = "Voice activity detection logo")
    private String vadModelId;

    @Schema(description = "Large language model identifier")
    private String llmModelId;

    @Schema(description = "VLLM model identification")
    private String vllmModelId;

    @Schema(description = "Speech synthesis model identification")
    private String ttsModelId;

    @Schema(description = "timbre identity")
    private String ttsVoiceId;

    @Schema(description = "memory model identifier")
    private String memModelId;

    @Schema(description = "Intent model identifier")
    private String intentModelId;

    @Schema(description = "Chat record configuration (0 does not record, 1 records text only, 2 records text and voice)")
    private Integer chatHistoryConf;

    @Schema(description = "Character setting parameters")
    private String systemPrompt;

    @Schema(description = "Summary memory", example = "Build a growable dynamic memory network, retain_critical_information_in_a_limited_space, evolution_track_of_intelligent_maintenance_information\n" +
            "Summarize_important_information_about_the_user based on conversation history to provide more personalized service in future conversations", required = false)
    private String summaryMemory;

    @Schema(description = "language encoding")
    private String langCode;

    @Schema(description = "interactive language")
    private String language;

    @Schema(description = "sort")
    private Integer sort;

    @Schema(description = "Creator")
    private Long creator;

    @Schema(description = "creation time")
    private Date createdAt;

    @Schema(description = "Updater")
    private Long updater;

    @Schema(description = "Update time")
    private Date updatedAt;
}