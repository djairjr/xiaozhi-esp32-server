package xiaozhi.modules.agent.dto;

import lombok.Data;

/**
 * modify_the_dto_of_the_agents_voiceprint
 *
 * @author zjy
 */
@Data
public class AgentVoicePrintUpdateDTO {
    /**
     * intelligent_voiceprint_id
     */
    private String id;
    /**
     * audio_file_id
     */
    private String audioId;
    /**
     * the_name_of_the_person_whose_voiceprint_comes_from
     */
    private String sourceName;
    /**
     * person_who_describes_the_source_of_the_voiceprint
     */
    private String introduce;
}
