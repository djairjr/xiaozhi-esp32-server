package xiaozhi.modules.agent.service;

import java.util.List;

import com.baomidou.mybatisplus.extension.service.IService;

import xiaozhi.modules.agent.entity.AgentPluginMapping;

/*
*
* @description for_table【ai_agent_plugin_mapping (unique mapping table between Agent and plug-in)】database_operation_service
 * @createDate 2025-05-25 22:33:17
*/
public interface AgentPluginMappingService extends IService<AgentPluginMapping> {

    /**
     * get_plugin_parameters_based_on_agent_id
     * 
     * @param agentId
     * @return
     */
    List<AgentPluginMapping> agentPluginParamsByAgentId(String agentId);

    /**
     * delete_plugin_parameters_based_on_agent_id
     * 
     * @param agentId
     */
    void deleteByAgentId(String agentId);
}
