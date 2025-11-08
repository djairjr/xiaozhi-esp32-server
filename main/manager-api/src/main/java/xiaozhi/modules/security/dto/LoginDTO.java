package xiaozhi.modules.security.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * login_form
 */
@Data
@Schema(description = "Login form")
public class LoginDTO implements Serializable {

    @Schema(description = "phone number")
    @NotBlank(message = "{sysuser.username.require}")
    private String username;

    @Schema(description = "password")
    @NotBlank(message = "{sysuser.password.require}")
    private String password;

    @Schema(description = "Mobile phone verification code")
    private String mobileCaptcha;

    @Schema(description = "unique identifier")
    @NotBlank(message = "{sysuser.uuid.require}")
    private String captchaId;

}