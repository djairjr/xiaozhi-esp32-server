package xiaozhi.modules.agent.entity;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

/**
 * agent_chat_audio_datasheet
 *
 * @author Goody
 * @version 1.0, 2025/5/8
 * @since 1.0.0
 */
@Data
@TableName("ai_agent_chat_audio")
public class AgentChatAudioEntity {
    /**
     * primary_key_id
     */
    @TableId(type = IdType.ASSIGN_UUID)
    private String id;

    /**
     * audio_opus_data
     */
    private byte[] audio;
}