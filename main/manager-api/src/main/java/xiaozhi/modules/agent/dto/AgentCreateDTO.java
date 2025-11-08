package xiaozhi.modules.agent.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/*
*
 * agent_creates_dto
* dedicated_to_adding_new_agents, does_not_contain_id, agentCode and sort fields, these_fields_are_automatically_generated_by_the_system/set_default_value
*/
@Data
@Schema(description = "Agent creates objects")
public class AgentCreateDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "Agent name", example = "Customer service assistant")
    @NotBlank(message = "Agent name cannot be empty")
    private String agentName;
}