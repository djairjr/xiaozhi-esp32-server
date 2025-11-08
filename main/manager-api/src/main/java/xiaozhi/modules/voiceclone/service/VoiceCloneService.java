package xiaozhi.modules.voiceclone.service;

import java.util.List;
import java.util.Map;

import org.springframework.web.multipart.MultipartFile;

import xiaozhi.common.page.PageData;
import xiaozhi.common.service.BaseService;
import xiaozhi.modules.voiceclone.dto.VoiceCloneDTO;
import xiaozhi.modules.voiceclone.dto.VoiceCloneResponseDTO;
import xiaozhi.modules.voiceclone.entity.VoiceCloneEntity;

/**
 * sound_clone_management
 */
public interface VoiceCloneService extends BaseService<VoiceCloneEntity> {

    /**
     * page_query
     */
    PageData<VoiceCloneEntity> page(Map<String, Object> params);

    /**
     * save_sound_clone
     */
    void save(VoiceCloneDTO dto);

    /**
     * batch_delete
     */
    void delete(String[] ids);

    /**
     * query_the_list_of_sound_clones_based_on_user_id
     * 
     * @param userId user_id
     * @return sound_clone_list
     */
    List<VoiceCloneEntity> getByUserId(Long userId);

    /**
     * paginated_query_for_sound_clone_list_with_model_name_and_user_name
     */
    PageData<VoiceCloneResponseDTO> pageWithNames(Map<String, Object> params);

    /**
     * query_sound_clone_information_with_model_name_and_user_name_based_on_id
     */
    VoiceCloneResponseDTO getByIdWithNames(String id);

    /**
     * query_the_list_of_sound_clones_with_model_name_based_on_user_id
     */
    List<VoiceCloneResponseDTO> getByUserIdWithNames(Long userId);

    /**
     * upload_audio_files
     */
    void uploadVoice(String id, MultipartFile voiceFile) throws Exception;

    /**
     * update_sound_clone_names
     */
    void updateName(String id, String name);

    /**
     * get_audio_data
     */
    byte[] getVoiceData(String id);

    /**
     * clone_audio，call_the_volcano_engine_for_voice_reproduction_training
     * 
     * @param cloneId voice_clone_record_id
     */
    void cloneAudio(String cloneId);
}
