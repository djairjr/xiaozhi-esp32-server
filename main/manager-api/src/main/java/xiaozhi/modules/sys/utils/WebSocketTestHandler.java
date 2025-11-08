package xiaozhi.modules.sys.utils;

import java.util.concurrent.CompletableFuture;

import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.WebSocketHandler;
import org.springframework.web.socket.WebSocketMessage;
import org.springframework.web.socket.WebSocketSession;

public class WebSocketTestHandler implements WebSocketHandler {
    private final CompletableFuture<Boolean> future;

    public WebSocketTestHandler(CompletableFuture<Boolean> future) {
        this.future = future;
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        future.complete(true);
        try {
            session.close();
        } catch (Exception e) {
            // ignore_shutdown_exception
        }
    }

    @Override
    public void handleMessage(WebSocketSession session, WebSocketMessage<?> message) {
        // no_need_to_process_messages
    }

    @Override
    public void handleTransportError(WebSocketSession session, Throwable exception) {
        future.complete(false);
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus closeStatus) {
        // no_processing_is_done_when_the_connection_is_closed
    }

    @Override
    public boolean supportsPartialMessages() {
        return false;
    }
}