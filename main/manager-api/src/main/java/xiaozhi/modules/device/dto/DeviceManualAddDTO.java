package xiaozhi.modules.device.dto;

import lombok.Data;

@Data
public class DeviceManualAddDTO {
    private String agentId;
    private String board;        // device_model
    private String appVersion;   // firmware_version
    private String macAddress;   // Mac address
} 