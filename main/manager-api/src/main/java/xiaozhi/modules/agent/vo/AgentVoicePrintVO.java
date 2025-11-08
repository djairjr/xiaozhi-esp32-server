package xiaozhi.modules.agent.vo;

import lombok.Data;

import java.util.Date;

/**
 * display_the_agent_voiceprint_list_vo
 */
@Data
public class AgentVoicePrintVO {

    /**
     * primary_key_id
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
    /**
     * creation_time
     */
    private Date createDate;
}
