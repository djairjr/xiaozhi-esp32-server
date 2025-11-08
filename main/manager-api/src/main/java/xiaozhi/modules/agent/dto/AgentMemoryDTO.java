package xiaozhi.modules.agent.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * agent_memory_update_dto
 */
@Data
@Schema(description = "Agent memory update object")
public class AgentMemoryDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "Summary memory", example = "Build a growable dynamic memory network, retain_critical_information_in_a_limited_space, evolution_track_of_intelligent_maintenance_information\n" +
            "Summarize_important_information_about_the_user based on conversation history to provide more personalized service in future conversations", required = false)
    private String summaryMemory;
}