package xiaozhi.modules.sys.dto;

import lombok.Data;
import xiaozhi.modules.sys.enums.ServerActionEnum;

import java.util.Map;

/**
 * server_action_dto
 */
@Data
public class ServerActionPayloadDTO
{
    /**
    * type（what_the_smart_console_sends_to_the_server_is_server）
    */
    private String type;
    /**
    * action
    */
    private ServerActionEnum action;
    /**
    * content
    */
    private Map<String, Object> content;

    public static ServerActionPayloadDTO build(ServerActionEnum action, Map<String, Object> content) {
        ServerActionPayloadDTO serverActionPayloadDTO = new ServerActionPayloadDTO();
        serverActionPayloadDTO.setAction(action);
        serverActionPayloadDTO.setContent(content);
        serverActionPayloadDTO.setType("server");
        return serverActionPayloadDTO;
    }
    // privatization
    private ServerActionPayloadDTO() {}
}
