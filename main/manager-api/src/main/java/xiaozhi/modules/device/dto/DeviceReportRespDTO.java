package xiaozhi.modules.device.dto;

import io.swagger.v3.oas.annotations.media.Schema;
import lombok.Data;
import lombok.Getter;
import lombok.Setter;

@Data
@Schema(description = "Device OTA detection version return body, including activation code requirements")
public class DeviceReportRespDTO {
    @Schema(description = "server time")
    private ServerTime server_time;

    @Schema(description = "activation code")
    private Activation activation;

    @Schema(description = "error message")
    private String error;

    @Schema(description = "Firmware version information")
    private Firmware firmware;

    @Schema(description = "WebSocket configuration")
    private Websocket websocket;

    @Schema(description = "MQTT Gateway configuration")
    private MQTT mqtt;

    @Getter
    @Setter
    public static class Firmware {
        @Schema(description = "version number")
        private String version;
        @Schema(description = "Download address")
        private String url;
    }

    public static DeviceReportRespDTO createError(String message) {
        DeviceReportRespDTO resp = new DeviceReportRespDTO();
        resp.setError(message);
        return resp;
    }

    @Setter
    @Getter
    public static class Activation {
        @Schema(description = "activation code")
        private String code;

        @Schema(description = "Activation code information: Activation address")
        private String message;

        @Schema(description = "Challenge code")
        private String challenge;
    }

    @Getter
    @Setter
    public static class ServerTime {
        @Schema(description = "Timestamp")
        private Long timestamp;

        @Schema(description = "time zone")
        private String timeZone;

        @Schema(description = "Time zone offset in minutes")
        private Integer timezone_offset;
    }

    @Getter
    @Setter
    public static class Websocket {
        @Schema(description = "WebSocket server address")
        private String url;
        @Schema(description = "WebSocket certification token")
        private String token;
    }

    @Getter
    @Setter
    public static class MQTT {
        @Schema(description = "MQTT configuration URL")
        private String endpoint;
        @Schema(description = "MQTT client unique identifier")
        private String client_id;
        @Schema(description = "MQTT authentication username")
        private String username;
        @Schema(description = "MQTT authentication password")
        private String password;
        @Schema(description = "ESP32 publishes messages to topics")
        private String publish_topic;
        @Schema(description = "Topics subscribed by ESP32")
        private String subscribe_topic;
    }
}