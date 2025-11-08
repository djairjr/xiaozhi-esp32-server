package xiaozhi.modules.timbre.service;

import java.util.List;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.model.dto.VoiceDTO;
import xiaozhi.modules.timbre.dto.TimbreDataDTO;
import xiaozhi.modules.timbre.dto.TimbrePageDTO;
import xiaozhi.modules.timbre.entity.TimbreEntity;
import xiaozhi.modules.timbre.vo.TimbreDetailsVO;

/**
 * definition_of_timbre_business_layer
 * 
 * @author zjy
 * @since 2025-3-21
 */
public interface TimbreService extends BaseService<TimbreEntity> {
    /**
     * paginate_to_obtain_the_timbre_under_the_specified_timbre_tts
     * 
     * @param dto pagination_search_parameters
     * @return tone_list_paging_data
     */
    PageData<TimbreDetailsVO> page(TimbrePageDTO dto);

    /**
     * get_detailed_information_about_the_specified_id_of_the_timbre
     * 
     * @param timbreId timbre_table_id
     * @return timbre_information
     */
    TimbreDetailsVO get(String timbreId);

    /**
     * save_sound_information
     * 
     * @param dto need_to_save_data
     */
    void save(TimbreDataDTO dto);

    /**
     * save_sound_information
     * 
     * @param timbreId id_that_needs_to_be_modified
     * @param dto      data_that_needs_to_be_modified
     */
    void update(String timbreId, TimbreDataDTO dto);

    /**
     * delete_sounds_in_batches
     * 
     * @param ids list_of_timbre_ids_that_need_to_be_deleted
     */
    void delete(String[] ids);

    List<VoiceDTO> getVoiceNames(String ttsModelId, String voiceName);

    /**
     * get_the_timbre_name_based_on_id
     * 
     * @param id tone_id
     * @return voice_name
     */
    String getTimbreNameById(String id);

    /**
     * obtain_timbre_information_based_on_timbre_encoding
     * 
     * @param ttsModelId tone_model_id
     * @param voiceCode  timbre_encoding
     * @return timbre_information
     */
    VoiceDTO getByVoiceCode(String ttsModelId, String voiceCode);
}