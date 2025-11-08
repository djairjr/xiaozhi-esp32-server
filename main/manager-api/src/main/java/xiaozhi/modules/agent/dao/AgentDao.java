package xiaozhi.modules.agent.dao;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import org.apache.ibatis.annotations.Select;
import xiaozhi.common.dao.BaseDao;
import xiaozhi.modules.agent.entity.AgentEntity;
import xiaozhi.modules.agent.vo.AgentInfoVO;

@Mapper
public interface AgentDao extends BaseDao<AgentEntity> {
    /**
     * get_the_number_of_devices_of_the_agent
     * 
     * @param agentId agent_id
     * @return number_of_devices
     */
    Integer getDeviceCountByAgentId(@Param("agentId") String agentId);

    /**
     * query_the_default_agent_information_of_the_corresponding_device_based_on_the_device_mac_address
     *
     * @param macAddress device_mac_address
     * @return default_agent_information
     */
    @Select(" SELECT a.* FROM ai_device d " +
            " LEFT JOIN ai_agent a ON d.agent_id = a.id " +
            " WHERE d.mac_address = #{macAddress} " +
            " ORDER BY d.id DESC LIMIT 1")
    AgentEntity getDefaultAgentByMacAddress(@Param("macAddress") String macAddress);

    /**
     * query_agent_information_based_on_id，includes_plugin_information
     *
     * @param agentId agent_id
     */
    AgentInfoVO selectAgentInfoById(@Param("agentId") String agentId);
}
