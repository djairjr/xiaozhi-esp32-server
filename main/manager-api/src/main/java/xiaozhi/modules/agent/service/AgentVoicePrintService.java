package xiaozhi.modules.agent.service;

import java.util.List;

import xiaozhi.modules.agent.dto.AgentVoicePrintSaveDTO;
import xiaozhi.modules.agent.dto.AgentVoicePrintUpdateDTO;
import xiaozhi.modules.agent.vo.AgentVoicePrintVO;

/**
 * intelligent_voiceprint_processing_service
 *
 * @author zjy
 */
public interface AgentVoicePrintService {
    /**
     * add_a_new_voiceprint_for_the_agent
     *
     * @param dto save_the_data_of_the_agents_voiceprint
     * @return T:success F：fail
     */
    boolean insert(AgentVoicePrintSaveDTO dto);

    /**
     * delete_the_voiceprint_of_the_agents_finger
     *
     * @param userId       the_currently_logged_in_user_id
     * @param voicePrintId voiceprint_id
     * @return is_it_successful T:success F：fail
     */
    boolean delete(Long userId, String voicePrintId);

    /**
     * get_all_voiceprint_data_of_the_specified_agent
     *
     * @param userId  the_currently_logged_in_user_id
     * @param agentId agent_id
     * @return voiceprint_data_collection
     */
    List<AgentVoicePrintVO> list(Long userId, String agentId);

    /**
     * update_the_agents_finger_voiceprint_data
     *
     * @param userId the_currently_logged_in_user_id
     * @param dto    modified_voiceprint_data
     * @return is_it_successful T:success F：fail
     */
    boolean update(Long userId, AgentVoicePrintUpdateDTO dto);

}
