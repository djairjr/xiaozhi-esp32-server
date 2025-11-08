package xiaozhi.modules.sys.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.io.Serializable;

/**
 * retrieve_password_dto
 */
@Data
@Schema(description = "Retrieve password")
public class RetrievePasswordDTO implements Serializable {

    @Schema(description = "phone number")
    @NotBlank(message = "{sysuser.password.require}")
    private String phone;

    @Schema(description = "Verification code")
    @NotBlank(message = "{sysuser.password.require}")
    private String code;

    @Schema(description = "New Password")
    @NotBlank(message = "{sysuser.password.require}")
    private String password;

    @Schema(description = "Graphic verification code ID")
    @NotBlank(message = "{sysuser.uuid.require}")
    private String captchaId;



}