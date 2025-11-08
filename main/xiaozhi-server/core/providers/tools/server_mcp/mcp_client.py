"""Server MCP client"""

from __future__ import annotations

from datetime import timedelta
import asyncio
import os
import shutil
import concurrent.futures
from contextlib import AsyncExitStack
from typing import Optional, List, Dict, Any

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client
from mcp.client.streamable_http import streamablehttp_client
from config.logger import setup_logging
from core.utils.util import sanitize_tool_name

TAG = __name__


class ServerMCPClient:
    """Server-side MCP client, used to connect and manage MCP services"""

    def __init__(self, config: Dict[str, Any]):
        """Initialize the server MCP client

        Args:
            config: MCP service configuration dictionary"""
        self.logger = setup_logging()
        self.config = config

        self._worker_task: Optional[asyncio.Task] = None
        self._ready_evt = asyncio.Event()
        self._shutdown_evt = asyncio.Event()

        self.session: Optional[ClientSession] = None
        self.tools: List = []  # original tool object
        self.tools_dict: Dict[str, Any] = {}
        self.name_mapping: Dict[str, str] = {}

    async def initialize(self):
        """Initialize MCP client connection"""
        if self._worker_task:
            return

        self._worker_task = asyncio.create_task(
            self._worker(), name="ServerMCPClientWorker"
        )
        await self._ready_evt.wait()

        self.logger.bind(tag=TAG).info(
            f"The server MCP client is connected, available tools: {[name for name in self.name_mapping.values()]}"
        )

    async def cleanup(self):
        """Clean up MCP client resources"""
        if not self._worker_task:
            return

        self._shutdown_evt.set()
        try:
            await asyncio.wait_for(self._worker_task, timeout=20)
        except (asyncio.TimeoutError, Exception) as e:
            self.logger.bind(tag=TAG).error(f"Server MCP client shutdown error: {e}")
        finally:
            self._worker_task = None

    def has_tool(self, name: str) -> bool:
        """Check if the specified tool is included

        Args:
            name: tool name

        Returns:
            bool: whether to include this tool"""
        return name in self.tools_dict

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """Get definitions of all available tools

        Returns:
            List[Dict[str, Any]]: tool definition list"""
        return [
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": tool.description,
                    "parameters": tool.inputSchema,
                },
            }
            for name, tool in self.tools_dict.items()
        ]

    async def call_tool(self, name: str, args: dict) -> Any:
        """Call the specified tool

        Args:
            name: tool name
            args: tool parameters

        Returns:
            Any: tool execution result

        Raises:
            RuntimeError: thrown when the client is not initialized"""
        if not self.session:
            raise RuntimeError("Server MCP client is not initialized")

        real_name = self.name_mapping.get(name, name)
        loop = self._worker_task.get_loop()
        coro = self.session.call_tool(real_name, args)

        if loop is asyncio.get_running_loop():
            return await coro

        fut: concurrent.futures.Future = asyncio.run_coroutine_threadsafe(coro, loop)
        return await asyncio.wrap_future(fut)

    def is_connected(self) -> bool:
        """Check whether the MCP client is connected properly

        Returns:
            bool: Returns True if the client is connected and working normally, otherwise returns False"""
        # Check if the work task exists
        if self._worker_task is None:
            return False

        # Check if a work task has been completed or canceled
        if self._worker_task.done():
            return False

        # Check if the session exists
        if self.session is None:
            return False

        # All checks passed and the connection is normal
        return True

    async def _worker(self):
        """MCP client work coroutine"""
        async with AsyncExitStack() as stack:
            try:
                # Create StdioClient
                if "command" in self.config:
                    cmd = (
                        shutil.which("npx")
                        if self.config["command"] == "npx"
                        else self.config["command"]
                    )
                    env = {**os.environ, **self.config.get("env", {})}
                    params = StdioServerParameters(
                        command=cmd,
                        args=self.config.get("args", []),
                        env=env,
                    )
                    stdio_r, stdio_w = await stack.enter_async_context(
                        stdio_client(params)
                    )
                    read_stream, write_stream = stdio_r, stdio_w

                # Create SSEClient
                elif "url" in self.config:
                    headers = dict(self.config.get("headers", {}))
                    # TODO compatible with older versions
                    if "API_ACCESS_TOKEN" in self.config:
                        headers["Authorization"] = f"Bearer {self.config['API_ACCESS_TOKEN']}"
                        self.logger.bind(tag=TAG).warning(f"You are using the old outdated configuration API_ACCESS_TOKEN, please set API_ACCESS_TOKEN directly in the headers in .mcp_server_settings.json, for example 'Authorization': 'Bearer API_ACCESS_TOKEN'")
                   
                    # Select different clients according to the transport type, the default is SSE
                    transport_type = self.config.get("transport", "sse")

                    if transport_type == "streamable-http" or transport_type == "http":
                        # Using Streamable HTTP transport
                        http_r, http_w, get_session_id = await stack.enter_async_context(
                            streamablehttp_client(
                                url=self.config["url"],
                                headers=headers,
                                timeout=self.config.get("timeout", 30),
                                sse_read_timeout=self.config.get("sse_read_timeout", 60 * 5),
                                terminate_on_close=self.config.get("terminate_on_close", True)
                            )
                        )
                        read_stream, write_stream = http_r, http_w
                    else:
                        # Using traditional SSE transport
                        sse_r, sse_w = await stack.enter_async_context(
                            sse_client(
                                url=self.config["url"],
                                headers=headers,
                                timeout=self.config.get("timeout", 5),
                                sse_read_timeout=self.config.get("sse_read_timeout", 60 * 5)
                            )
                        )
                        read_stream, write_stream = sse_r, sse_w

                else:
                    raise ValueError("MCP client configuration must contain 'command' or 'url'")

                self.session = await stack.enter_async_context(
                    ClientSession(
                        read_stream=read_stream,
                        write_stream=write_stream,
                        read_timeout_seconds=timedelta(seconds=15),
                    )
                )
                await self.session.initialize()

                # Get tools
                self.tools = (await self.session.list_tools()).tools
                for t in self.tools:
                    sanitized = sanitize_tool_name(t.name)
                    self.tools_dict[sanitized] = t
                    self.name_mapping[sanitized] = t.name

                self._ready_evt.set()

                # pending shutdown
                await self._shutdown_evt.wait()

            except Exception as e:
                self.logger.bind(tag=TAG).error(f"Server MCP client worker coroutine error: {e}")
                self._ready_evt.set()
                raise
