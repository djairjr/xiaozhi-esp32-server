package xiaozhi.modules.agent.entity;

import java.util.Date;

import com.baomidou.mybatisplus.annotation.FieldFill;
import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import lombok.Data;

/**
 * intelligent_voiceprint_table
 *
 * @author zjy
 */
@TableName(value = "ai_agent_voice_print")
@Data
public class AgentVoicePrintEntity {
    /**
     * primary_key_id
     */
    @TableId(type = IdType.ASSIGN_UUID)
    private String id;
    /**
     * associated_agent_id
     */
    private String agentId;
    /**
     * associated_audio_id
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
     * creator
     */
    @TableField(fill = FieldFill.INSERT)
    private Long creator;
    /**
     * creation_time
     */
    @TableField(fill = FieldFill.INSERT)
    private Date createDate;

    /**
     * updater
     */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Long updater;
    /**
     * update_time
     */
    @TableField(fill = FieldFill.INSERT_UPDATE)
    private Date updateDate;
}
