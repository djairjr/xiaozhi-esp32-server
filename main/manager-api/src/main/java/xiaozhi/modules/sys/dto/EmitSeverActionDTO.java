package xiaozhi.modules.sys.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotEmpty;
import jakarta.validation.constraints.NotNull;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import xiaozhi.modules.sys.enums.ServerActionEnum;

/**
 * send_python_server_operation_dto
 */
@Data
@NoArgsConstructor
@AllArgsConstructor
public class EmitSeverActionDTO
{
    @Schema(description = "Target ws address")
    @NotEmpty(message = "The target ws address cannot be empty")
    private String targetWs;

    @Schema(description = "Specify operation")
    @NotNull(message = "Operation cannot be empty")
    private ServerActionEnum action;
}
