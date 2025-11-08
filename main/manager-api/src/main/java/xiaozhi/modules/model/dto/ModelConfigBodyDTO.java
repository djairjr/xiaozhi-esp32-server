package xiaozhi.modules.model.dto;

import java.io.Serial;

import cn.hutool.json.JSONObject;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

@Data
@Schema(description = "model provider/vendor")
public class ModelConfigBodyDTO {

    @Serial
    private static final long serialVersionUID = 1L;

    @Schema(description = "Model ID, if not filled in, it will be automatically generated")
    private String id;

    @Schema(description = "Model encoding (such_as_alillm, DoubaoTTS)")
    private String modelCode;

    @Schema(description = "Model name")
    private String modelName;

    @Schema(description = "Is it the default configuration (0 no 1 yes)")
    private Integer isDefault;

    @Schema(description = "Whether to enable")
    private Integer isEnabled;

    @Schema(description = "Model configuration (JSON format)")
    private JSONObject configJson;

    @Schema(description = "Official document link")
    private String docLink;

    @Schema(description = "Remark")
    private String remark;

    @Schema(description = "sort")
    private Integer sort;
}
