package xiaozhi.modules.agent.dao;

import org.apache.ibatis.annotations.Mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;

import xiaozhi.modules.agent.entity.AgentChatHistoryEntity;

/**
 * {@link AgentChatHistoryEntity} agent_chat_history_dao_object
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
@Mapper
public interface AiAgentChatHistoryDao extends BaseMapper<AgentChatHistoryEntity> {
    /**
     * delete_audio_based_on_agent_id
     *
     * @param agentId agent_id
     */
    void deleteAudioByAgentId(String agentId);

    /**
     * delete_chat_history_based_on_agent_id
     *
     * @param agentId agent_id
     */
    void deleteHistoryByAgentId(String agentId);

    /**
     * remove_audio_id_based_on_agent_id
     *
     * @param agentId agent_id
     */
    void deleteAudioIdByAgentId(String agentId);
}
