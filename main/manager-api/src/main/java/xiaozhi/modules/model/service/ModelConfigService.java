package xiaozhi.modules.model.service;

import java.util.List;
import java.util.Map;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.model.dto.LlmModelBasicInfoDTO;
import xiaozhi.modules.model.dto.ModelBasicInfoDTO;
import xiaozhi.modules.model.dto.ModelConfigBodyDTO;
import xiaozhi.modules.model.dto.ModelConfigDTO;
import xiaozhi.modules.model.entity.ModelConfigEntity;

public interface ModelConfigService extends BaseService<ModelConfigEntity> {

    List<ModelBasicInfoDTO> getModelCodeList(String modelType, String modelName);

    List<LlmModelBasicInfoDTO> getLlmModelCodeList(String modelName);

    PageData<ModelConfigDTO> getPageList(String modelType, String modelName, String page, String limit);

    ModelConfigDTO add(String modelType, String provideCode, ModelConfigBodyDTO modelConfigBodyDTO);

    ModelConfigDTO edit(String modelType, String provideCode, String id, ModelConfigBodyDTO modelConfigBodyDTO);

    void delete(String id);

    /**
     * get_model_name_based_on_id
     * 
     * @param id model_id
     * @return model_name
     */
    String getModelNameById(String id);

    /**
     * get_model_configuration_based_on_id
     * 
     * @param id model_id
     * @return model_configuration_entity
     */
    ModelConfigEntity getModelByIdFromCache(String id);

    /**
     * set_default_model
     *
     * @param modelType model_type
     * @param isDefault is_it_the_default（1:yes，0:no）
     */
    void setDefaultModel(String modelType, int isDefault);

    /*
*
     * get_a_list_of_eligible_tts_platforms
     *
* @return TTS platform list (id and modelName)
*/
    List<Map<String, Object>> getTtsPlatformList();
}
