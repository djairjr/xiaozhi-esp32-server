package xiaozhi.modules.voiceclone.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.baomidou.mybatisplus.core.mapper.BaseMapper;

import xiaozhi.modules.model.dto.VoiceDTO;
import xiaozhi.modules.voiceclone.entity.VoiceCloneEntity;

/**
 * sound_cloning
 */
@Mapper
public interface VoiceCloneDao extends BaseMapper<VoiceCloneEntity> {
    /**
     * get_the_list_of_timbres_successfully_trained_by_the_user
     * 
     * @param modelId model_id
     * @param userId  user_id
     * @return successfully_trained_timbre_list
     */
    List<VoiceDTO> getTrainSuccess(String modelId, Long userId);

}
