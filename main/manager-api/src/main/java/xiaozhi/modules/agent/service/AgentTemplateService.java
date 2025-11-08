package xiaozhi.modules.agent.service;

import com.baomidou.mybatisplus.extension.service.IService;

import xiaozhi.modules.agent.entity.AgentTemplateEntity;

/**
 * @author chenerlei
 * @description for_table【ai_agent_template(agent_configuration_template_table)】database_operation_service
 * @createDate 2025-03-22 11:48:18
 */
public interface AgentTemplateService extends IService<AgentTemplateEntity> {

    /**
     * get_default_template
     * 
     * @return default_template_entity
     */
    AgentTemplateEntity getDefaultTemplate();

    /**
     * update_model_id_in_default_template
     * 
     * @param modelType model_type
     * @param modelId   model_id
     */
    void updateDefaultTemplateModelId(String modelType, String modelId);

    /**
     * reorder_remaining_templates_after_deleting_them
     * 
     * @param deletedSort sorting_value_of_deleted_template
     */
    void reorderTemplatesAfterDelete(Integer deletedSort);

    /**
     * get_the_next_available_sort_number（find_the_smallest_unused_sequence_number）
     * 
     * @return next_available_sort_sequence_number
     */
    Integer getNextAvailableSort();
}
