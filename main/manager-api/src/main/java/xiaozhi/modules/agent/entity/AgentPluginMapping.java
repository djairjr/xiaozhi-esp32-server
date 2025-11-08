package xiaozhi.modules.agent.entity;

import java.io.Serializable;

import com.baomidou.mybatisplus.annotation.IdType;
import com.baomidou.mybatisplus.annotation.TableField;
import com.baomidou.mybatisplus.annotation.TableId;
import com.baomidou.mybatisplus.annotation.TableName;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/*
*
* Unique mapping table between Agent and plug-in
 * 
 * @TableName ai_agent_plugin_mapping
*/
@Data
@TableName(value = "ai_agent_plugin_mapping")
@Schema(description = "Unique mapping table between Agent and plug-in")
public class AgentPluginMapping implements Serializable {
    /**
     * primary_key
     */
    @TableId(type = IdType.ASSIGN_ID)
    @Schema(description = "Mapping information primary key ID")
    private Long id;

    /**
     * agent_id
     */
    @Schema(description = "Agent ID")
    private String agentId;

    /**
     * plugin_id
     */
    @Schema(description = "Plugin ID")
    private String pluginId;

    /**
     * plugin_parameters(Json)format
     */
    @Schema(description = "Plug-in parameter (Json) format")
    private String paramInfo;

    // redundant_fields，used_to_facilitate_querying_plugins_based_on_id，check_the_provider_code_of_the_plugin,see_dao_layer_xml_file_for_details
    @TableField(exist = false)
    @Schema(description = "Plug-in provider_code, corresponding table ai_model_provider")
    private String providerCode;

    @TableField(exist = false)
    private static final long serialVersionUID = 1L;
}