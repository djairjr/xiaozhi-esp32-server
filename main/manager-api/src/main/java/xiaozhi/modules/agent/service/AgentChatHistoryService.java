package xiaozhi.modules.agent.service;

import java.util.List;
import java.util.Map;

import com.baomidou.mybatisplus.extension.service.IService;

import xiaozhi.common.page.PageData;
import xiaozhi.modules.agent.dto.AgentChatHistoryDTO;
import xiaozhi.modules.agent.dto.AgentChatSessionDTO;
import xiaozhi.modules.agent.entity.AgentChatHistoryEntity;
import xiaozhi.modules.agent.vo.AgentChatHistoryUserVO;

/**
 * agent_chat_record_table_processing_service
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
public interface AgentChatHistoryService extends IService<AgentChatHistoryEntity> {

    /**
     * get_session_list_based_on_agent_id
     *
     * @param params query_parameters，contains_agentid、page、limit
     * @return paginated_conversation_list
     */
    PageData<AgentChatSessionDTO> getSessionListByAgentId(Map<String, Object> params);

    /**
     * get_chat_history_list_based_on_session_id
     *
     * @param agentId   agent_id
     * @param sessionId session_id
     * @return chat_history_list
     */
    List<AgentChatHistoryDTO> getChatHistoryBySessionId(String agentId, String sessionId);

    /**
     * delete_chat_history_based_on_agent_id
     *
     * @param agentId     agent_id
     * @param deleteAudio whether_to_delete_audio
     * @param deleteText  whether_to_delete_text
     */
    void deleteByAgentId(String agentId, Boolean deleteAudio, Boolean deleteText);

    /**
     * get_the_latest_50_user_chat_history_data_based_on_the_agent_id（with_audio_data）
     *
     * @param agentId agent_id
     * @return chat_history_list（only_users）
     */
    List<AgentChatHistoryUserVO> getRecentlyFiftyByAgentId(String agentId);

    /**
     * get_chat_content_based_on_audio_data_id
     *
     * @param audioId audio_id
     * @return chat_content
     */
    String getContentByAudioId(String audioId);


    /**
     * query_whether_this_audio_id_belongs_to_this_agent
     *
     * @param audioId audio_id
     * @param agentId audio_id
     * @return T：belong F：does_not_belong
     */
    boolean isAudioOwnedByAgent(String audioId,String agentId);
}
