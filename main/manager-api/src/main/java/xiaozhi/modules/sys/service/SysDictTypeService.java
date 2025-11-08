package xiaozhi.modules.sys.service;

import java.util.List;
import java.util.Map;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.sys.dto.SysDictTypeDTO;
import xiaozhi.modules.sys.entity.SysDictTypeEntity;
import xiaozhi.modules.sys.vo.SysDictTypeVO;

/**
 * data_dictionary
 */
public interface SysDictTypeService extends BaseService<SysDictTypeEntity> {

    /**
     * query_dictionary_type_information_by_page
     *
     * @param params query_parameters，contains_paging_information_and_query_conditions
     * @return returns_paginated_dictionary_type_data
     */
    PageData<SysDictTypeVO> page(Map<String, Object> params);

    /**
     * get_dictionary_type_information_based_on_id
     *
     * @param id dictionary_type_id
     * @return returns_a_dictionary_type_object
     */
    SysDictTypeVO get(Long id);

    /**
     * save_dictionary_type_information
     *
     * @param dto dictionary_type_data_transfer_object
     */
    void save(SysDictTypeDTO dto);

    /**
     * update_dictionary_type_information
     *
     * @param dto dictionary_type_data_transfer_object
     */
    void update(SysDictTypeDTO dto);

    /**
     * delete_dictionary_type_information
     *
     * @param ids array_of_dictionary_type_ids_to_be_deleted
     */
    void delete(Long[] ids);

    /**
     * list_all_dictionary_type_information
     *
     * @return returns_a_list_of_dictionary_types
     */
    List<SysDictTypeVO> list(Map<String, Object> params);
}