package xiaozhi.modules.device.dao;

import java.util.Date;

import org.apache.ibatis.annotations.Mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;

import xiaozhi.modules.device.entity.DeviceEntity;

@Mapper
public interface DeviceDao extends BaseMapper<DeviceEntity> {
    /**
     * get_the_last_connection_time_of_all_devices_of_this_agent
     * 
     * @param agentId agent_id
     * @return
     */
    Date getAllLastConnectedAtByAgentId(String agentId);

}