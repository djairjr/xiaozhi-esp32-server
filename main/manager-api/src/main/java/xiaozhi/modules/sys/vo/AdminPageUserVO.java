package xiaozhi.modules.sys.vo;

import java.util.Date;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;

/**
 * the_administrator_displays_the_users_vo_in_pages
 * @ zjy
 * 
 * @since 2025-3-25
 */
@Data
public class AdminPageUserVO {

    @Schema(description = "Number of devices")
    private String deviceCount;

    @Schema(description = "phone number")
    private String mobile;

    @Schema(description = "state")
    private Integer status;

    @Schema(description = "user id")
    private String userid;

    @Schema(description = "Registration time")
    private Date createDate;
}
