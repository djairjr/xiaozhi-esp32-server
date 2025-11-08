package xiaozhi.modules.agent.service.biz;

import xiaozhi.modules.agent.dto.AgentChatHistoryReportDTO;

/**
 * agent_chat_history_business_logic_layer
 *
 * @author Goody
 * @version 1.0, 2025/4/30
 * @since 1.0.0
 */
public interface AgentChatHistoryBizService {

    /*
*
     * chat_reporting_method
     *
     * @param agentChatHistoryReportDTO input_object_containing_information_required_for_chat_reporting
     *                                  for_example：device_mac_address、file_type、content_etc
* @return upload_results, true indicates success, false indicates failure
*/
    Boolean report(AgentChatHistoryReportDTO agentChatHistoryReportDTO);
}
