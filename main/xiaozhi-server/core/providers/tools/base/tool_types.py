"""Type definitions for tool systems"""

from enum import Enum

from dataclasses import dataclass
from typing import Any, Dict, Optional
from plugins_func.register import Action


class ToolType(Enum):
    """Tool type enum"""

    SERVER_PLUGIN = "server_plugin"  # Server plug-in
    SERVER_MCP = "server_mcp"  # Server MCP
    DEVICE_IOT = "device_iot"  # Device-side IoT
    DEVICE_MCP = "device_mcp"  # Device side MCP
    MCP_ENDPOINT = "mcp_endpoint"  # MCP access point


@dataclass
class ToolDefinition:
    """Tool definition"""

    name: str  # Tool name
    description: Dict[str, Any]  # Tool description (OpenAI function call format)
    tool_type: ToolType  # Tool type
    parameters: Optional[Dict[str, Any]] = None  # extra parameters
