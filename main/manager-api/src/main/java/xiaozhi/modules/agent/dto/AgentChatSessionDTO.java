package xiaozhi.modules.agent.dto;

import java.time.LocalDateTime;

import lombok.Data;

/**
 * agent_session_list_dto
 */
@Data
public class AgentChatSessionDTO {
    /**
     * session_id
     */
    private String sessionId;

    /**
     * session_time
     */
    private LocalDateTime createdAt;

    /**
     * number_of_chats
     */
    private Integer chatCount;
}