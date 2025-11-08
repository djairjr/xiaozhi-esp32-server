package xiaozhi.modules.agent.dto;

import lombok.Data;

/**
 * save_the_dto_of_the_agents_voiceprint
 *
 * @author zjy
 */
@Data
public class AgentVoicePrintSaveDTO {
    /**
     * associated_agent_id
     */
    private String agentId;
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
