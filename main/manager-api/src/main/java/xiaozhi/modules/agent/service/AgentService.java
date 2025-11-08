package xiaozhi.modules.agent.service;

import java.util.List;
import java.util.Map;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.agent.dto.AgentCreateDTO;
import xiaozhi.modules.agent.dto.AgentDTO;
import xiaozhi.modules.agent.dto.AgentUpdateDTO;
import xiaozhi.modules.agent.entity.AgentEntity;
import xiaozhi.modules.agent.vo.AgentInfoVO;

/**
 * intelligent_body_surface_treatment_service
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
public interface AgentService extends BaseService<AgentEntity> {
    /**
     * get_the_list_of_administrator_agents
     *
     * @param params query_parameters
     * @return paginated_data
     */
    PageData<AgentEntity> adminAgentList(Map<String, Object> params);

    /**
     * get_the_agent_based_on_id
     *
     * @param id agent_id
     * @return agent_entity
     */
    AgentInfoVO getAgentById(String id);

    /**
     * insert_agent
     *
     * @param entity agent_entity
     * @return is_it_successful
     */
    boolean insert(AgentEntity entity);

    /**
     * delete_agent_based_on_user_id
     *
     * @param userId user_id
     */
    void deleteAgentByUserId(Long userId);

    /**
     * get_the_list_of_user_agents
     *
     * @param userId user_id
     * @return agent_list
     */
    List<AgentDTO> getUserAgents(Long userId);

    /**
     * get_the_number_of_devices_based_on_the_agent_id
     *
     * @param agentId agent_id
     * @return number_of_devices
     */
    Integer getDeviceCountByAgentId(String agentId);

    /**
     * query_the_default_agent_information_of_the_corresponding_device_based_on_the_device_mac_address
     *
     * @param macAddress device_mac_address
     * @return default_agent_information，returns_null_if_it_does_not_exist
     */
    AgentEntity getDefaultAgentByMacAddress(String macAddress);

    /**
     * check_if_the_user_has_permission_to_access_the_agent
     *
     * @param agentId agent_id
     * @param userId  user_id
     * @return do_you_have_permission
     */
    boolean checkAgentPermission(String agentId, Long userId);

    /**
     * update_agent
     *
     * @param agentId agent_id
     * @param dto     update_the_information_needed_by_the_agent
     */
    void updateAgentById(String agentId, AgentUpdateDTO dto);

    /**
     * create_an_agent
     *
     * @param dto information_needed_to_create_the_agent
     * @return created_agent_id
     */
    String createAgent(AgentCreateDTO dto);
}
