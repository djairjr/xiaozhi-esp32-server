package xiaozhi.modules.device.dto;

import java.io.Serializable;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

/**
 * device_unbinding_form
 */
@Data
@Schema(description = "Device unbinding form")
public class DeviceUnBindDTO implements Serializable {

    @Schema(description = "Device ID")
    @NotBlank(message = "Device ID cannot be empty")
    private String deviceId;

}