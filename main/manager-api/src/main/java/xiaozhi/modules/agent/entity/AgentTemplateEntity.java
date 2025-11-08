package xiaozhi.modules.agent.entity;

import java.io.Serializable;
import java.util.Date;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

/**
 * agent_configuration_template_table
 * 
 * @TableName ai_agent_template
 */
@TableName(value = "ai_agent_template")
@Data
public class AgentTemplateEntity implements Serializable {
    /**
     * agent_unique_identifier
     */
    @TableId(type = IdType.ASSIGN_UUID)
    private String id;

    /**
     * agent_coding
     */
    private String agentCode;

    /**
     * agent_name
     */
    private String agentName;

    /**
     * speech_recognition_model_identification
     */
    private String asrModelId;

    /**
     * voice_activity_detection_logo
     */
    private String vadModelId;

    /**
     * large_language_model_identifier
     */
    private String llmModelId;

    /*
*
* VLLM model identification
*/
    private String vllmModelId;

    /**
     * speech_synthesis_model_identification
     */
    private String ttsModelId;

    /**
     * timbre_identity
     */
    private String ttsVoiceId;

    /**
     * memory_model_identifier
     */
    private String memModelId;

    /**
     * intent_model_identifier
     */
    private String intentModelId;

    /*
*
* chat_history_configuration (0 does not record 1 records text only 2 records text and voice)
*/
    private Integer chatHistoryConf;

    /**
     * character_setting_parameters
     */
    private String systemPrompt;

    /**
     * summary_memory
     */
    private String summaryMemory;
    /**
     * language_encoding
     */
    private String langCode;

    /**
     * interactive_language
     */
    private String language;

    /**
     * sorting_weight
     */
    private Integer sort;

    /**
     * creator ID
     */
    private Long creator;

    /**
     * creation_time
     */
    private Date createdAt;

    /**
     * updater ID
     */
    private Long updater;

    /**
     * update_time
     */
    private Date updatedAt;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}