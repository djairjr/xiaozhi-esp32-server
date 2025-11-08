package xiaozhi.modules.sys.service;

import java.util.List;
import java.util.Map;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.sys.dto.SysParamsDTO;
import xiaozhi.modules.sys.entity.SysParamsEntity;

/**
 * parameter_management
 */
public interface SysParamsService extends BaseService<SysParamsEntity> {

    PageData<SysParamsDTO> page(Map<String, Object> params);

    List<SysParamsDTO> list(Map<String, Object> params);

    SysParamsDTO get(Long id);

    void save(SysParamsDTO dto);

    void update(SysParamsDTO dto);

    void delete(String[] ids);

    /**
     * coding_according_to_parameters，get_the_value_of_the_parameter
     *
     * @param paramCode parameter_encoding
     * @param fromCache whether_to_obtain_from_cache
     */
    String getValue(String paramCode, Boolean fromCache);

    /*
*
     * coding_according_to_parameters，get_the_object_object_of_value
     *
     * @param paramCode parameter_encoding
* @param clazz Object object
*/
    <T> T getValueObject(String paramCode, Class<T> clazz);

    /**
     * coding_according_to_parameters，update_value
     *
     * @param paramCode  parameter_encoding
     * @param paramValue parameter_value
     */
    int updateValueByCode(String paramCode, String paramValue);

    /**
     * initialize_server_key
     */
    void initServerSecret();
}
