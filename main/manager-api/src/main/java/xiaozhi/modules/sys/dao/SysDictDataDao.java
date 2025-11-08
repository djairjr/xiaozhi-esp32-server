package xiaozhi.modules.sys.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import xiaozhi.common.dao.BaseDao;
import xiaozhi.modules.sys.entity.SysDictDataEntity;
import xiaozhi.modules.sys.vo.SysDictDataItem;

/**
 * dictionary_data
 */
@Mapper
public interface SysDictDataDao extends BaseDao<SysDictDataEntity> {

    List<SysDictDataItem> getDictDataByType(String dictType);

    /**
     * get_dictionary_type_encoding_based_on_dictionary_type_id
     * 
     * @param dictTypeId dictionary_type_id
     * @return dictionary_type_encoding
     */
    String getTypeByTypeId(Long dictTypeId);
}
