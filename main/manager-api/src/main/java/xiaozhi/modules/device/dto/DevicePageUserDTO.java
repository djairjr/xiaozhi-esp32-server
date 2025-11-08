package xiaozhi.modules.device.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import lombok.Data;

/**
 * query_the_dto_of_all_devices
 * 
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Query the DTO of all devices")
public class DevicePageUserDTO {

    @Schema(description = "Equipment keywords")
    private String keywords;

    @Schema(description = "Number of pages")
    @Min(value = 0, message = "{page.number}")
    private String page;

    @Schema(description = "Display number of columns")
    @Min(value = 0, message = "{limit.number}")
    private String limit;
}
