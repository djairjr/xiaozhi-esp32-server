package xiaozhi.modules.sys.vo;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * dictionary_data_vo
 */
@Data
@Schema(description = "Dictionary data items")
public class SysDictDataItem implements Serializable {

    @Schema(description = "dictionary tag")
    private String name;

    @Schema(description = "Dictionary value")
    private String key;
}
