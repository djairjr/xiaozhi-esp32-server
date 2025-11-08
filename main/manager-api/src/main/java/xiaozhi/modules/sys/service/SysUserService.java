package xiaozhi.modules.sys.service;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.sys.dto.AdminPageUserDTO;
import xiaozhi.modules.sys.dto.PasswordDTO;
import xiaozhi.modules.sys.dto.SysUserDTO;
import xiaozhi.modules.sys.entity.SysUserEntity;
import xiaozhi.modules.sys.vo.AdminPageUserVO;

/**
 * system_user
 */
public interface SysUserService extends BaseService<SysUserEntity> {

    SysUserDTO getByUsername(String username);

    SysUserDTO getByUserId(Long userId);

    void save(SysUserDTO dto);

    /**
     * delete_specified_user，and_associated_data_devices_and_agents
     * 
     * @param ids
     */
    void deleteById(Long ids);

    /**
     * verify_if_password_changes_are_allowed
     * 
     * @param userId      user_id
     * @param passwordDTO password_verification_parameters
     */
    void changePassword(Long userId, PasswordDTO passwordDTO);

    /**
     * change_password_directly，no_verification_required
     * 
     * @param userId   user_id
     * @param password password
     */
    void changePasswordDirectly(Long userId, String password);

    /**
     * reset_password
     * 
     * @param userId user_id
     * @return randomly_generate_passwords_that_comply_with_specifications
     */
    String resetPassword(Long userId);

    /**
     * administrator_paging_user_information
     * 
     * @param dto pagination_search_parameters
     * @return user_list_pagination_data
     */
    PageData<AdminPageUserVO> page(AdminPageUserDTO dto);

    /**
     * modify_user_status_in_batches
     * 
     * @param status  user_status
     * @param userIds user_id_array
     */
    void changeStatus(Integer status, String[] userIds);

    /**
     * get_whether_user_registration_is_allowed
     * 
     * @return whether_to_allow_user_registration
     */
    boolean getAllowUserRegister();
}
