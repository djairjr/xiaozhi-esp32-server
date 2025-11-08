"""Server MCP Manager"""

import asyncio
import os
import json
from typing import Dict, Any, List
from config.config_loader import get_project_dir
from config.logger import setup_logging
from .mcp_client import ServerMCPClient

TAG = __name__
logger = setup_logging()


class ServerMCPManager:
    """Centralized manager for managing multiple server-side MCP services"""

    def __init__(self, conn) -> None:
        """Initialize MCP Manager"""
        self.conn = conn
        self.config_path = get_project_dir() + "data/.mcp_server_settings.json"
        if not os.path.exists(self.config_path):
            self.config_path = ""
            logger.bind(tag=TAG).warning(
                f"Please check the mcp service configuration file: data/.mcp_server_settings.json"
            )
        self.clients: Dict[str, ServerMCPClient] = {}
        self.tools = []

    def load_config(self) -> Dict[str, Any]:
        """Load MCP service configuration"""
        if len(self.config_path) == 0:
            return {}

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
            return config.get("mcpServers", {})
        except Exception as e:
            logger.bind(tag=TAG).error(
                f"Error loading MCP config from {self.config_path}: {e}"
            )
            return {}

    async def initialize_servers(self) -> None:
        """Initialize all MCP services"""
        config = self.load_config()
        for name, srv_config in config.items():
            if not srv_config.get("command") and not srv_config.get("url"):
                logger.bind(tag=TAG).warning(
                    f"Skipping server {name}: neither command nor url specified"
                )
                continue

            try:
                # Initialize the server MCP client
                logger.bind(tag=TAG).info(f"Initialize server MCP client: {name}")
                client = ServerMCPClient(srv_config)
                await client.initialize()
                self.clients[name] = client
                client_tools = client.get_available_tools()
                self.tools.extend(client_tools)

            except Exception as e:
                logger.bind(tag=TAG).error(
                    f"Failed to initialize MCP server {name}: {e}"
                )

        # Output the list of currently supported server-side MCP tools
        if hasattr(self.conn, "func_handler") and self.conn.func_handler:
            # Refresh the tool cache to ensure that the server-side MCP tool is loaded correctly
            if hasattr(self.conn.func_handler, "tool_manager"):
                self.conn.func_handler.tool_manager.refresh_tools()
            self.conn.func_handler.current_support_functions()

    def get_all_tools(self) -> List[Dict[str, Any]]:
        """Get tool function definitions for all services"""
        return self.tools

    def is_mcp_tool(self, tool_name: str) -> bool:
        """Check if it is an MCP tool"""
        for tool in self.tools:
            if (
                tool.get("function") is not None
                and tool["function"].get("name") == tool_name
            ):
                return True
        return False

    async def execute_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute the tool call and try to reconnect if it fails"""
        logger.bind(tag=TAG).info(f"Execute the server-side MCP tool {tool_name}, parameters: {arguments}")

        max_retries = 3  # Maximum number of retries
        retry_interval = 2  # Retry interval (seconds)

        # Find the corresponding client
        client_name = None
        target_client = None
        for name, client in self.clients.items():
            if client.has_tool(tool_name):
                client_name = name
                target_client = client
                break

        if not target_client:
            raise ValueError(f"Tool {tool_name} not found in any MCP service")

        # Tool call with retry mechanism
        for attempt in range(max_retries):
            try:
                return await target_client.call_tool(tool_name, arguments)
            except Exception as e:
                # Throw an exception directly when the last attempt fails
                if attempt == max_retries - 1:
                    raise

                logger.bind(tag=TAG).warning(
                    f"Failed to execute tool {tool_name} (attempt {attempt+1}/{max_retries}): {e}"
                )

                # Try to reconnect
                logger.bind(tag=TAG).info(
                    f"Try to reconnect to MCP client {client_name} before retrying"
                )
                try:
                    # close old connection
                    await target_client.cleanup()

                    # Reinitialize client
                    config = self.load_config()
                    if client_name in config:
                        client = ServerMCPClient(config[client_name])
                        await client.initialize()
                        self.clients[client_name] = client
                        target_client = client
                        logger.bind(tag=TAG).info(
                            f"Successfully reconnected MCP client: {client_name}"
                        )
                    else:
                        logger.bind(tag=TAG).error(
                            f"Cannot reconnect MCP client {client_name}: config not found"
                        )
                except Exception as reconnect_error:
                    logger.bind(tag=TAG).error(
                        f"Failed to reconnect MCP client {client_name}: {reconnect_error}"
                    )

                # Wait for some time and try again
                await asyncio.sleep(retry_interval)

    async def cleanup_all(self) -> None:
        """Close all MCP clients"""
        for name, client in list(self.clients.items()):
            try:
                if hasattr(client, "cleanup"):
                    await asyncio.wait_for(client.cleanup(), timeout=20)
                logger.bind(tag=TAG).info(f"Server MCP client has been closed: {name}")
            except (asyncio.TimeoutError, Exception) as e:
                logger.bind(tag=TAG).error(f"Error closing server MCP client {name}: {e}")
        self.clients.clear()
