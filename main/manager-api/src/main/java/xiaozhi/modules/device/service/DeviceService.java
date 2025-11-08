package xiaozhi.modules.device.service;

import java.util.Date;
import java.util.List;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.device.dto.DevicePageUserDTO;
import xiaozhi.modules.device.dto.DeviceReportReqDTO;
import xiaozhi.modules.device.dto.DeviceReportRespDTO;
import xiaozhi.modules.device.dto.DeviceManualAddDTO;
import xiaozhi.modules.device.entity.DeviceEntity;
import xiaozhi.modules.device.vo.UserShowDeviceListVO;

public interface DeviceService extends BaseService<DeviceEntity> {

    /**
     * check_if_the_device_is_activated
     */
    DeviceReportRespDTO checkDeviceActive(String macAddress, String clientId,
            DeviceReportReqDTO deviceReport);

    /**
     * get_the_device_list_of_the_userspecified_agent，
     */
    List<DeviceEntity> getUserDevices(Long userId, String agentId);

    /**
     * unbind_device
     */
    void unbindDevice(Long userId, String deviceId);

    /**
     * device_activation
     */
    Boolean deviceActivation(String agentId, String activationCode);

    /**
     * delete_all_devices_for_this_user
     * 
     * @param userId user_id
     */
    void deleteByUserId(Long userId);

    /**
     * delete_all_devices_associated_with_the_specified_agent
     * 
     * @param agentId agent_id
     */
    void deleteByAgentId(String agentId);

    /**
     * get_the_number_of_devices_of_a_specified_user
     * 
     * @param userId user_id
     * @return number_of_devices
     */
    Long selectCountByUserId(Long userId);

    /**
     * get_all_device_information_in_pages
     *
     * @param dto pagination_search_parameters
     * @return user_list_pagination_data
     */
    PageData<UserShowDeviceListVO> page(DevicePageUserDTO dto);

    /*
*
     * get_device_information_based_on_mac_address
     * 
* @param macAddress MAC address
     * @return device_information
*/
    DeviceEntity getDeviceByMacAddress(String macAddress);

    /**
     * get_activation_code_based_on_device_id
     * 
     * @param deviceId device_id
     * @return activation_code
     */
    String geCodeByDeviceId(String deviceId);

    /**
     * get_the_most_recent_last_connection_time_for_this_smart_device
     * @param agentId agent_id
     * @return returns_the_devices_most_recent_last_connection_time
     */
    Date getLatestLastConnectionTime(String agentId);

    /**
     * add_device_manually
     */
    void manualAddDevice(Long userId, DeviceManualAddDTO dto);

    /**
     * update_device_connection_information
     */
    void updateDeviceConnectionInfo(String agentId, String deviceId, String appVersion);

}