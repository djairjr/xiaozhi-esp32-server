import sys
import uuid
import signal
import asyncio
from aioconsole import ainput
from config.settings import load_config
from config.logger import setup_logging
from core.utils.util import get_local_ip, validate_mcp_endpoint
from core.http_server import SimpleHttpServer
from core.websocket_server import WebSocketServer
from core.utils.util import check_ffmpeg_installed

TAG = __name__
logger = setup_logging()


async def wait_for_exit() -> None:
    """Blocks until Ctrl‑C / SIGTERM is received.
    - Unix: use add_signal_handler
    - Windows: depends on KeyboardInterrupt"""
    loop = asyncio.get_running_loop()
    stop_event = asyncio.Event()

    if sys.platform != "win32":  # Unix / macOS
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, stop_event.set)
        await stop_event.wait()
    else:
        # Windows: await a fut that is always pending,
        # Let KeyboardInterrupt bubble up to asyncio.run to eliminate the problem of legacy normal threads blocking process exits
        try:
            await asyncio.Future()
        except KeyboardInterrupt:  # Ctrl‑C
            pass


async def monitor_stdin():
    """Monitor standard input and consume the Enter key"""
    while True:
        await ainput()  # Asynchronously wait for input, consume and press Enter


async def main():
    check_ffmpeg_installed()
    config = load_config()

    # auth_key priority: Configuration file server.auth_key > manager-api.secret > automatically generated
    # auth_key is used for jwt authentication, such as jwt authentication of the visual analysis interface, token generation and websocket authentication of the ota interface
    # Get the auth_key in the configuration file
    auth_key = config["server"].get("auth_key", "")
    
    # Verify auth_key, if invalid, try to use manager-api.secret
    if not auth_key or len(auth_key) == 0 or "you" in auth_key:
        auth_key = config.get("manager-api", {}).get("secret", "")
        # Verify the secret, if invalid, generate a random key
        if not auth_key or len(auth_key) == 0 or "you" in auth_key:
            auth_key = str(uuid.uuid4().hex)
    
    config["server"]["auth_key"] = auth_key

    # Add stdin monitoring task
    stdin_task = asyncio.create_task(monitor_stdin())

    # Start the WebSocket server
    ws_server = WebSocketServer(config)
    ws_task = asyncio.create_task(ws_server.start())
    # Start Simple http server
    ota_server = SimpleHttpServer(config)
    ota_task = asyncio.create_task(ota_server.start())

    read_config_from_api = config.get("read_config_from_api", False)
    port = int(config["server"].get("http_port", 8003))
    if not read_config_from_api:
        logger.bind(tag=TAG).info(
            "The OTA interface is\t\thttp://{}:{}/xiaozhi/ota/",
            get_local_ip(),
            port,
        )
    logger.bind(tag=TAG).info(
        "The visual analysis interface is\thttp://{}:{}/mcp/vision/explain",
        get_local_ip(),
        port,
    )
    mcp_endpoint = config.get("mcp_endpoint", None)
    if mcp_endpoint is not None and "you" not in mcp_endpoint:
        # Verify MCP access point format
        if validate_mcp_endpoint(mcp_endpoint):
            logger.bind(tag=TAG).info("mcp access point is\t{}", mcp_endpoint)
            # Convert mcp counting point address into call point
            mcp_endpoint = mcp_endpoint.replace("/mcp/", "/call/")
            config["mcp_endpoint"] = mcp_endpoint
        else:
            logger.bind(tag=TAG).error("mcp access point does not comply with specifications")
            config["mcp_endpoint"] = "Your access point websocket address"

    # Get WebSocket configuration, use safe defaults
    websocket_port = 8000
    server_config = config.get("server", {})
    if isinstance(server_config, dict):
        websocket_port = int(server_config.get("port", 8000))

    logger.bind(tag=TAG).info(
        "The Websocket address is\tws://{}:{}/xiaozhi/v1/",
        get_local_ip(),
        websocket_port,
    )

    logger.bind(tag=TAG).info(
        "=======The above address is the websocket protocol address, please do not use a browser to access it========"
    )
    logger.bind(tag=TAG).info(
        "If you want to test websocket, please use Google Chrome to open test_page.html in the test directory."
    )
    logger.bind(tag=TAG).info(
        "=============================================================\n"
    )

    try:
        await wait_for_exit()  # Block until exit signal is received
    except asyncio.CancelledError:
        print("The task was canceled and resources are being cleaned...")
    finally:
        # Cancel all tasks (key fix point)
        stdin_task.cancel()
        ws_task.cancel()
        if ota_task:
            ota_task.cancel()

        # Wait for task termination (timeout must be added)
        await asyncio.wait(
            [stdin_task, ws_task, ota_task] if ota_task else [stdin_task, ws_task],
            timeout=3.0,
            return_when=asyncio.ALL_COMPLETED,
        )
        print("The server has been shut down and the program has exited.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Manual interruption, the program terminates.")
