package xiaozhi.modules.agent.service;

import com.baomidou.mybatisplus.extension.service.IService;

import xiaozhi.modules.agent.entity.AgentChatAudioEntity;

/**
 * agent_chat_audio_data_table_processing_service
 *
 * @author Goody
 * @version 1.0, 2025/5/8
 * @since 1.0.0
 */
public interface AgentChatAudioService extends IService<AgentChatAudioEntity> {
    /**
     * save_audio_data
     *
     * @param audioData audio_data
     * @return audio_id
     */
    String saveAudio(byte[] audioData);

    /**
     * get_audio_data
     *
     * @param audioId audio_id
     * @return audio_data
     */
    byte[] getAudio(String audioId);
}
