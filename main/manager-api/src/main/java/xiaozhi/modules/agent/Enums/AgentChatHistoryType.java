package xiaozhi.modules.agent.Enums;


import lombok.Getter;

/**
 * agent_chat_record_type
 */
@Getter
public enum AgentChatHistoryType {

    USER((byte) 1),
    AGENT((byte) 2);

    private final byte value;

    AgentChatHistoryType(byte i) {
        this.value = i;
    }

}
