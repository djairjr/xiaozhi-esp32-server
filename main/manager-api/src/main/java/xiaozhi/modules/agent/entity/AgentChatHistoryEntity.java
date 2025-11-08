package xiaozhi.modules.agent.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

/**
 * agent_chat_record_table
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor
@TableName(value = "ai_agent_chat_history")
public class AgentChatHistoryEntity {
    /**
     * primary_key_id
     */
    @TableId(type = IdType.AUTO)
    private Long id;

    /*
*
*MAC address
*/
    @TableField(value = "mac_address")
    private String macAddress;

    /**
     * agent_id
     */
    @TableField(value = "agent_id")
    private String agentId;

    /**
     * session_id
     */
    @TableField(value = "session_id")
    private String sessionId;

    /**
     * message_type: 1-user, 2-agent
     */
    @TableField(value = "chat_type")
    private Byte chatType;

    /**
     * chat_content
     */
    @TableField(value = "content")
    private String content;

    /**
     * audio_base64_data
     */
    @TableField(value = "audio_id")
    private String audioId;

    /**
     * creation_time
     */
    @TableField(value = "created_at")
    private Date createdAt;

    /**
     * update_time
     */
    @TableField(value = "updated_at")
    private Date updatedAt;
}
