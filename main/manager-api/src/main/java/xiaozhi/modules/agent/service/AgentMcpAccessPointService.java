package xiaozhi.modules.agent.service;


import java.util.List;

/**
 * agent_mcp_access_point_processing_service
 *
 * @author zjy
 */
public interface AgentMcpAccessPointService {
    /*
*
     * get_the_agents_mcp_access_point_address
     * @param id agent_id
* @return mcp access point address
*/
   String getAgentMcpAccessAddress(String id);

    /**
     * get_the_existing_tool_list_of_the_agents_mcp_access_point
     * @param id agent_id
     * @return tool_list
     */
   List<String> getAgentMcpToolsList(String id);
}
