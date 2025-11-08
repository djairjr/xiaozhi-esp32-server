package xiaozhi.modules.sys.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * dictionary_type_vo
 */
@Data
@Schema(description = "Dictionary type VO")
public class SysDictTypeVO implements Serializable {
    @Schema(description = "primary key")
    private Long id;

    @Schema(description = "dictionary type")
    private String dictType;

    @Schema(description = "Dictionary name")
    private String dictName;

    @Schema(description = "Remark")
    private String remark;

    @Schema(description = "sort")
    private Integer sort;

    @Schema(description = "Creator")
    private Long creator;

    @Schema(description = "Creator name")
    private String creatorName;

    @Schema(description = "creation time")
    private Date createDate;

    @Schema(description = "Updater")
    private Long updater;

    @Schema(description = "Updater name")
    private String updaterName;

    @Schema(description = "Update time")
    private Date updateDate;
}
