package xiaozhi.modules.sys.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Min;
import lombok.Data;

/**
 * parameter_dto_for_admin_pagination_user
 * 
 * @author zjy
 * @since 2025-3-21
 */
@Data
@Schema(description = "Parameter DTO for admin pagination user")
public class AdminPageUserDTO {

    @Schema(description = "phone number")
    private String mobile;

    @Schema(description = "Number of pages")
    @Min(value = 0, message = "{sort.number}")
    private String page;

    @Schema(description = "Display number of columns")
    @Min(value = 0, message = "{sort.number}")
    private String limit;
}
