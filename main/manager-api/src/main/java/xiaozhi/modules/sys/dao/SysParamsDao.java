package xiaozhi.modules.sys.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import xiaozhi.common.dao.BaseDao;
import xiaozhi.modules.sys.entity.SysParamsEntity;

/**
 * parameter_management
 */
@Mapper
public interface SysParamsDao extends BaseDao<SysParamsEntity> {
    /**
     * coding_according_to_parameters，query_value
     *
     * @param paramCode parameter_encoding
     * @return parameter_value
     */
    String getValueByCode(String paramCode);

    /**
     * get_parameter_encoding_list
     *
     * @param ids ids
     * @return return_parameter_encoding_list
     */
    List<String> getParamCodeList(String[] ids);

    /**
     * coding_according_to_parameters，update_value
     *
     * @param paramCode  parameter_encoding
     * @param paramValue parameter_value
     */
    int updateValueByCode(@Param("paramCode") String paramCode, @Param("paramValue") String paramValue);
}
