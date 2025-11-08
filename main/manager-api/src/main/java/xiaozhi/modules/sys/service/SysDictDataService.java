package xiaozhi.modules.sys.service;

import java.util.List;
import java.util.Map;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.sys.dto.SysDictDataDTO;
import xiaozhi.modules.sys.entity.SysDictDataEntity;
import xiaozhi.modules.sys.vo.SysDictDataItem;
import xiaozhi.modules.sys.vo.SysDictDataVO;

/**
 * data_dictionary
 */
public interface SysDictDataService extends BaseService<SysDictDataEntity> {

    /**
     * query_data_dictionary_information_by_page
     *
     * @param params query_parameters，contains_paging_information_and_query_conditions
     * @return returns_the_paginated_query_results_of_the_data_dictionary
     */
    PageData<SysDictDataVO> page(Map<String, Object> params);

    /**
     * get_data_dictionary_entity_based_on_id
     *
     * @param id the_unique_identifier_of_the_data_dictionary_entity
     * @return returns_details_of_a_data_dictionary_entity
     */
    SysDictDataVO get(Long id);

    /**
     * save_new_data_dictionary_entry
     *
     * @param dto saved_data_transfer_object_for_data_dictionary_items
     */
    void save(SysDictDataDTO dto);

    /**
     * update_data_dictionary_entry
     *
     * @param dto update_data_transfer_object_for_data_dictionary_items
     */
    void update(SysDictDataDTO dto);

    /**
     * delete_data_dictionary_entry
     *
     * @param ids array_of_ids_of_data_dictionary_items_to_delete
     */
    void delete(Long[] ids);

    /**
     * delete_the_corresponding_dictionary_data_according_to_the_dictionary_type_id
     *
     * @param dictTypeId dictionary_type_id
     */
    void deleteByTypeId(Long dictTypeId);

    /**
     * get_dictionary_data_list_based_on_dictionary_type
     *
     * @param dictType dictionary_type
     * @return return_dictionary_data_list
     */
    List<SysDictDataItem> getDictDataByType(String dictType);

}