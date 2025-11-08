package xiaozhi.modules.sys.service;


import java.util.function.Consumer;

/**
 * define_a_system_user_tool_class，avoid_circular_dependencies_with_user_modules
 * if_users_and_devices_depend_on_each_other，user_needs_to_get_all_devices，the_device_in_turn_needs_to_obtain_the_username_of_each_device
 * @author zjy
 * @since 2025-4-2
 */
public interface SysUserUtilService {
    /**
     * assign_username
     * @param userId user_id
     * @param setter assignment_method
     */
    void assignUsername( Long userId, Consumer<String> setter);
}
