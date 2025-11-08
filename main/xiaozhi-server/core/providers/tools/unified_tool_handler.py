"""unified tool processor"""

import json
from typing import Dict, List, Any, Optional
from config.logger import setup_logging
from plugins_func.loadplugins import auto_import_modules

from .base import ToolType
from plugins_func.register import Action, ActionResponse
from .unified_tool_manager import ToolManager
from .server_plugins import ServerPluginExecutor
from .server_mcp import ServerMCPExecutor
from .device_iot import DeviceIoTExecutor
from .device_mcp import DeviceMCPExecutor
from .mcp_endpoint import MCPEndpointExecutor


class UnifiedToolHandler:
    """unified tool processor"""

    def __init__(self, conn):
        self.conn = conn
        self.config = conn.config
        self.logger = setup_logging()

        # Create tool manager
        self.tool_manager = ToolManager(conn)

        # Create various types of executors
        self.server_plugin_executor = ServerPluginExecutor(conn)
        self.server_mcp_executor = ServerMCPExecutor(conn)
        self.device_iot_executor = DeviceIoTExecutor(conn)
        self.device_mcp_executor = DeviceMCPExecutor(conn)
        self.mcp_endpoint_executor = MCPEndpointExecutor(conn)

        # Register executor
        self.tool_manager.register_executor(
            ToolType.SERVER_PLUGIN, self.server_plugin_executor
        )
        self.tool_manager.register_executor(
            ToolType.SERVER_MCP, self.server_mcp_executor
        )
        self.tool_manager.register_executor(
            ToolType.DEVICE_IOT, self.device_iot_executor
        )
        self.tool_manager.register_executor(
            ToolType.DEVICE_MCP, self.device_mcp_executor
        )
        self.tool_manager.register_executor(
            ToolType.MCP_ENDPOINT, self.mcp_endpoint_executor
        )

        # initialization flag
        self.finish_init = False

    async def _initialize(self):
        """Asynchronous initialization"""
        try:
            # Automatically import plug-in modules
            auto_import_modules("plugins_func.functions")

            # Initialize server MCP
            await self.server_mcp_executor.initialize()

            # Initialize MCP access point
            await self._initialize_mcp_endpoint()

            # Initialize Home Assistant (if needed)
            self._initialize_home_assistant()

            self.finish_init = True
            self.logger.info("Unified tool processor initialization completed")

            # Output a list of all currently supported tools
            self.current_support_functions()

        except Exception as e:
            self.logger.error(f"Unified tools processor initialization failed: {e}")

    async def _initialize_mcp_endpoint(self):
        """Initialize MCP access point"""
        try:
            from .mcp_endpoint import connect_mcp_endpoint

            # Get MCP access point URL from configuration
            mcp_endpoint_url = self.config.get("mcp_endpoint", "")

            if (
                mcp_endpoint_url
                and "your" not in mcp_endpoint_url
                and mcp_endpoint_url != "null"
            ):
                self.logger.info(f"Initializing MCP access point: {mcp_endpoint_url}")
                mcp_endpoint_client = await connect_mcp_endpoint(
                    mcp_endpoint_url, self.conn
                )

                if mcp_endpoint_client:
                    # Save MCP access point client into connection object
                    self.conn.mcp_endpoint_client = mcp_endpoint_client
                    self.logger.info("MCP access point initialization successful")
                else:
                    self.logger.warning("MCP access point initialization failed")

        except Exception as e:
            self.logger.error(f"Failed to initialize MCP access point: {e}")

    def _initialize_home_assistant(self):
        """Initialize Home Assistant prompt word"""
        try:
            from plugins_func.functions.hass_init import append_devices_to_prompt

            append_devices_to_prompt(self.conn)
        except ImportError:
            pass  # Ignore import errors
        except Exception as e:
            self.logger.error(f"Failed to initialize Home Assistant: {e}")

    def get_functions(self) -> List[Dict[str, Any]]:
        """Get function descriptions for all tools"""
        return self.tool_manager.get_function_descriptions()

    def current_support_functions(self) -> List[str]:
        """Get the list of currently supported function names"""
        func_names = self.tool_manager.get_supported_tool_names()
        self.logger.info(f"Currently supported function list: {func_names}")
        return func_names

    def upload_functions_desc(self):
        """Refresh function description list"""
        self.tool_manager.refresh_tools()
        self.logger.info("The function description list has been refreshed")

    def has_tool(self, tool_name: str) -> bool:
        """Check if there is a specified tool"""
        return self.tool_manager.has_tool(tool_name)

    async def handle_llm_function_call(
        self, conn, function_call_data: Dict[str, Any]
    ) -> Optional[ActionResponse]:
        """Handling LLM function calls"""
        try:
            # Handle multiple function calls
            if "function_calls" in function_call_data:
                responses = []
                for call in function_call_data["function_calls"]:
                    result = await self.tool_manager.execute_tool(
                        call["name"], call.get("arguments", {})
                    )
                    responses.append(result)
                return self._combine_responses(responses)

            # Handle single function call
            function_name = function_call_data["name"]
            arguments = function_call_data.get("arguments", {})

            # If arguments are strings, try to parse to JSON
            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments) if arguments else {}
                except json.JSONDecodeError:
                    self.logger.error(f"Unable to parse function arguments: {arguments}")
                    return ActionResponse(
                        action=Action.ERROR,
                        response="Unable to parse function parameters",
                    )

            self.logger.debug(f"Call function: {function_name}, parameters: {arguments}")

            # Execute tool call
            result = await self.tool_manager.execute_tool(function_name, arguments)
            return result

        except Exception as e:
            self.logger.error(f"Handling function call errors: {e}")
            return ActionResponse(action=Action.ERROR, response=str(e))

    def _combine_responses(self, responses: List[ActionResponse]) -> ActionResponse:
        """Combine responses from multiple function calls"""
        if not responses:
            return ActionResponse(action=Action.NONE, response="No response")

        # If there are any errors, return the first error
        for response in responses:
            if response.action == Action.ERROR:
                return response

        # Merge all successful responses
        contents = []
        responses_text = []

        for response in responses:
            if response.content:
                contents.append(response.content)
            if response.response:
                responses_text.append(response.response)

        # Determine the final action type
        final_action = Action.RESPONSE
        for response in responses:
            if response.action == Action.REQLLM:
                final_action = Action.REQLLM
                break

        return ActionResponse(
            action=final_action,
            result="; ".join(contents) if contents else None,
            response="; ".join(responses_text) if responses_text else None,
        )

    async def register_iot_tools(self, descriptors: List[Dict[str, Any]]):
        """Register IoT device tool"""
        self.device_iot_executor.register_iot_tools(descriptors)
        self.tool_manager.refresh_tools()
        self.logger.info(f"Tools that have registered {len(descriptors)} IoT devices")

    def get_tool_statistics(self) -> Dict[str, int]:
        """Get tool statistics"""
        return self.tool_manager.get_tool_statistics()

    async def cleanup(self):
        """Clean up resources"""
        try:
            await self.server_mcp_executor.cleanup()

            # Clean up MCP access point connections
            if (
                hasattr(self.conn, "mcp_endpoint_client")
                and self.conn.mcp_endpoint_client
            ):
                await self.conn.mcp_endpoint_client.close()

            self.logger.info("Tool processor cleanup completed")
        except Exception as e:
            self.logger.error(f"Tool processor cleanup failed: {e}")
