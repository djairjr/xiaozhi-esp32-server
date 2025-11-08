package xiaozhi.modules.sys.vo;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

import java.io.Serializable;
import java.util.Date;

/**
 * dictionary_data_vo
 */
@Data
@Schema(description = "Dictionary data VO")
public class SysDictDataVO implements Serializable {
    @Schema(description = "primary key")
    private Long id;

    @Schema(description = "Dictionary type ID")
    private Long dictTypeId;

    @Schema(description = "dictionary tag")
    private String dictLabel;

    @Schema(description = "Dictionary value")
    private String dictValue;

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
