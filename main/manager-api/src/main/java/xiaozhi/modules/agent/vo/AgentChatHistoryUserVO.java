package xiaozhi.modules.agent.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * vo_of_the_agent_users_personal_chat_data
 */
@Data
public class AgentChatHistoryUserVO {
    @Schema(description = "Chat content")
    private String content;

    @Schema(description = "Audio ID")
    private String audioId;
}
