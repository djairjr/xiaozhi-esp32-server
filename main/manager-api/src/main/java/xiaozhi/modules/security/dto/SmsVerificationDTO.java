package xiaozhi.modules.security.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * sms_verification_code_request_dto
 */
@Data
@Schema(description = "SMS verification code request")
public class SmsVerificationDTO implements Serializable {
    private static final long serialVersionUID = 1L;

    @Schema(description = "phone number")
    @NotBlank(message = "{sysuser.username.require}")
    private String phone;

    @Schema(description = "Verification code")
    @NotBlank(message = "{sysuser.captcha.require}")
    private String captcha;

    @Schema(description = "unique identifier")
    @NotBlank(message = "{sysuser.uuid.require}")
    private String captchaId;
}