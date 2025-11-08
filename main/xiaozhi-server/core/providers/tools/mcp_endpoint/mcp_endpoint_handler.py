"""MCP access point processor"""

import json
import asyncio
import re
import websockets
from config.logger import setup_logging
from .mcp_endpoint_client import MCPEndpointClient

TAG = __name__
logger = setup_logging()


async def connect_mcp_endpoint(mcp_endpoint_url: str, conn=None) -> MCPEndpointClient:
    """Connect to MCP access point"""
    if not mcp_endpoint_url or "your" in mcp_endpoint_url or mcp_endpoint_url == "null":
        return None

    try:
        websocket = await websockets.connect(mcp_endpoint_url)

        mcp_client = MCPEndpointClient(conn)
        mcp_client.set_websocket(websocket)

        # Start message listener
        asyncio.create_task(_message_listener(mcp_client))

        # Send initialization message
        await send_mcp_endpoint_initialize(mcp_client)

        # Send initialization completion notification
        await send_mcp_endpoint_notification(mcp_client, "notifications/initialized")

        # Get a list of tools
        await send_mcp_endpoint_tools_list(mcp_client)

        logger.bind(tag=TAG).info("MCP access point connection successful")
        return mcp_client

    except Exception as e:
        logger.bind(tag=TAG).error(f"Failed to connect to MCP access point: {e}")
        return None


async def _message_listener(mcp_client: MCPEndpointClient):
    """Listen for MCP access point messages"""
    try:
        async for message in mcp_client.websocket:
            await handle_mcp_endpoint_message(mcp_client, message)
    except websockets.exceptions.ConnectionClosed:
        logger.bind(tag=TAG).info("MCP access point connection closed")
    except Exception as e:
        logger.bind(tag=TAG).error(f"MCP access point message listener error: {e}")
    finally:
        await mcp_client.set_ready(False)


async def handle_mcp_endpoint_message(mcp_client: MCPEndpointClient, message: str):
    """Handling MCP access point messages"""
    try:
        payload = json.loads(message)
        logger.bind(tag=TAG).debug(f"MCP access point message received: {payload}")

        if not isinstance(payload, dict):
            logger.bind(tag=TAG).error("MCP access point message format error")
            return

        # Handle result
        if "result" in payload:
            result = payload["result"]
            # Safely get the message ID, use 0 if None
            msg_id_raw = payload.get("id")
            msg_id = int(msg_id_raw) if msg_id_raw is not None else 0

            # Check for tool call response first
            if msg_id in mcp_client.call_results:
                logger.bind(tag=TAG).debug(
                    f"Received tool call response, ID: {msg_id}, result: {result}"
                )
                await mcp_client.resolve_call_result(msg_id, result)
                return

            if msg_id == 1:  # mcpInitializeID
                logger.bind(tag=TAG).debug("MCP access point initialization response received")
                if result is not None and isinstance(result, dict):
                    server_info = result.get("serverInfo")
                    if isinstance(server_info, dict):
                        name = server_info.get("name")
                        version = server_info.get("version")
                        logger.bind(tag=TAG).info(
                            f"MCP access point server information: name={name}, version={version}"
                        )
                else:
                    logger.bind(tag=TAG).warning(
                        "The MCP access point initialization response result is empty or has an incorrect format."
                    )
                return

            elif msg_id == 2:  # mcpToolsListID
                logger.bind(tag=TAG).debug("MCP access point tool list response received")
                if (
                    result is not None
                    and isinstance(result, dict)
                    and "tools" in result
                ):
                    tools_data = result["tools"]
                    if not isinstance(tools_data, list):
                        logger.bind(tag=TAG).error("Tool list format error")
                        return

                    logger.bind(tag=TAG).info(
                        f"Number of tools supported by MCP access point: {len(tools_data)}"
                    )

                    for i, tool in enumerate(tools_data):
                        if not isinstance(tool, dict):
                            continue

                        name = tool.get("name", "")
                        description = tool.get("description", "")
                        input_schema = {
                            "type": "object",
                            "properties": {},
                            "required": [],
                        }

                        if "inputSchema" in tool and isinstance(
                            tool["inputSchema"], dict
                        ):
                            schema = tool["inputSchema"]
                            input_schema["type"] = schema.get("type", "object")
                            input_schema["properties"] = schema.get("properties", {})
                            input_schema["required"] = [
                                s
                                for s in schema.get("required", [])
                                if isinstance(s, str)
                            ]

                        new_tool = {
                            "name": name,
                            "description": description,
                            "inputSchema": input_schema,
                        }
                        await mcp_client.add_tool(new_tool)
                        logger.bind(tag=TAG).debug(f"MCP Access Point Tool #{i+1}: {name}")

                    # Replace tool name in all tool descriptions
                    for tool_data in mcp_client.tools.values():
                        if "description" in tool_data:
                            description = tool_data["description"]
                            # Iterate through all tool names to replace
                            for (
                                sanitized_name,
                                original_name,
                            ) in mcp_client.name_mapping.items():
                                description = description.replace(
                                    original_name, sanitized_name
                                )
                            tool_data["description"] = description

                    next_cursor = (
                        result.get("nextCursor", "") if result is not None else ""
                    )
                    if next_cursor:
                        logger.bind(tag=TAG).info(
                            f"There are more tools, nextCursor: {next_cursor}"
                        )
                        await send_mcp_endpoint_tools_list_continue(
                            mcp_client, next_cursor
                        )
                    else:
                        await mcp_client.set_ready(True)
                        logger.bind(tag=TAG).info(
                            "All MCP access point tools acquired, client ready"
                        )

                        # Refresh the tool cache to ensure that the MCP access point tool is included in the function list
                        if (
                            hasattr(mcp_client, "conn")
                            and mcp_client.conn
                            and hasattr(mcp_client.conn, "func_handler")
                            and mcp_client.conn.func_handler
                        ):
                            mcp_client.conn.func_handler.tool_manager.refresh_tools()
                            mcp_client.conn.func_handler.current_support_functions()

                        logger.bind(tag=TAG).info(
                            f"MCP access point tool acquisition completed, a total of {len(mcp_client.tools)} tools"
                        )
                else:
                    logger.bind(tag=TAG).warning(
                        "MCP access point tool list response result is empty or malformed"
                    )
                return

        # Handle method calls (requests from the endpoint)
        elif "method" in payload:
            method = payload["method"]
            logger.bind(tag=TAG).info(f"MCP access point request received: {method}")

        elif "error" in payload:
            error_data = payload["error"]
            error_msg = error_data.get("message", "unknown error")
            logger.bind(tag=TAG).error(f"Received MCP access point error response: {error_msg}")

            # Safely get the message ID, use 0 if None
            msg_id_raw = payload.get("id")
            msg_id = int(msg_id_raw) if msg_id_raw is not None else 0

            if msg_id in mcp_client.call_results:
                await mcp_client.reject_call_result(
                    msg_id, Exception(f"MCP access point error: {error_msg}")
                )

    except json.JSONDecodeError as e:
        logger.bind(tag=TAG).error(f"MCP access point message JSON parsing failed: {e}")
    except Exception as e:
        logger.bind(tag=TAG).error(f"Error while processing MCP access point message: {e}")
        import traceback

        logger.bind(tag=TAG).error(f"Error details: {traceback.format_exc()}")


async def send_mcp_endpoint_initialize(mcp_client: MCPEndpointClient):
    """Send MCP access point initialization message"""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,  # mcpInitializeID
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "roots": {"listChanged": True},
                "sampling": {},
            },
            "clientInfo": {
                "name": "XiaozhiMCPEndpointClient",
                "version": "1.0.0",
            },
        },
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).info("Send MCP access point initialization message")
    await mcp_client.send_message(message)


async def send_mcp_endpoint_notification(mcp_client: MCPEndpointClient, method: str):
    """Send MCP access point notification message"""
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": {},
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).debug(f"Send MCP access point notification: {method}")
    await mcp_client.send_message(message)


async def send_mcp_endpoint_tools_list(mcp_client: MCPEndpointClient):
    """Send MCP access point tool list request"""
    payload = {
        "jsonrpc": "2.0",
        "id": 2,  # mcpToolsListID
        "method": "tools/list",
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).debug("Send MCP access point tool list request")
    await mcp_client.send_message(message)


async def send_mcp_endpoint_tools_list_continue(
    mcp_client: MCPEndpointClient, cursor: str
):
    """Send MCP access point tool list request with cursor"""
    payload = {
        "jsonrpc": "2.0",
        "id": 2,  # mcpToolsListID (same ID for continuation)
        "method": "tools/list",
        "params": {"cursor": cursor},
    }
    message = json.dumps(payload)
    logger.bind(tag=TAG).info(f"Send MCP access point tool list request with cursor: {cursor}")
    await mcp_client.send_message(message)


async def call_mcp_endpoint_tool(
    mcp_client: MCPEndpointClient, tool_name: str, args: str = "{}", timeout: int = 30
):
    """Call the specified MCP access point tool and wait for the response"""
    if not await mcp_client.is_ready():
        raise RuntimeError("MCP access point client is not ready yet")

    if not mcp_client.has_tool(tool_name):
        raise ValueError(f"Tool {tool_name} does not exist")

    tool_call_id = await mcp_client.get_next_id()
    result_future = asyncio.Future()
    await mcp_client.register_call_result_future(tool_call_id, result_future)

    # Processing parameters
    try:
        if isinstance(args, str):
            # Make sure the string is valid JSON
            if not args.strip():
                arguments = {}
            else:
                try:
                    # Try to parse directly
                    arguments = json.loads(args)
                except json.JSONDecodeError:
                    # If parsing fails, try merging multiple JSON objects
                    try:
                        # Match all JSON objects using regular expression
                        json_objects = re.findall(r"\{[^{}]*\}", args)
                        if len(json_objects) > 1:
                            # Merge all JSON objects
                            merged_dict = {}
                            for json_str in json_objects:
                                try:
                                    obj = json.loads(json_str)
                                    if isinstance(obj, dict):
                                        merged_dict.update(obj)
                                except json.JSONDecodeError:
                                    continue
                            if merged_dict:
                                arguments = merged_dict
                            else:
                                raise ValueError(f"Unable to parse any valid JSON object: {args}")
                        else:
                            raise ValueError(f"Parameter JSON parsing failed: {args}")
                    except Exception as e:
                        logger.bind(tag=TAG).error(
                            f"Parameter JSON parsing failed: {str(e)}, original parameters: {args}"
                        )
                        raise ValueError(f"Parameter JSON parsing failed: {str(e)}")
        elif isinstance(args, dict):
            arguments = args
        else:
            raise ValueError(f"Wrong argument type, expected string or dictionary, actual type: {type(args)}")

        # Make sure the parameter is a dictionary type
        if not isinstance(arguments, dict):
            raise ValueError(f"Parameters must be dictionary type, actual type: {type(arguments)}")

    except Exception as e:
        if not isinstance(e, ValueError):
            raise ValueError(f"Parameter processing failed: {str(e)}")
        raise e

    actual_name = mcp_client.name_mapping.get(tool_name, tool_name)
    payload = {
        "jsonrpc": "2.0",
        "id": tool_call_id,
        "method": "tools/call",
        "params": {"name": actual_name, "arguments": arguments},
    }

    message = json.dumps(payload)
    logger.bind(tag=TAG).info(
        f"Send MCP access point tool call request: {actual_name}, parameters: {json.dumps(arguments, ensure_ascii=False)}"
    )
    await mcp_client.send_message(message)

    try:
        # Wait for response or timeout
        raw_result = await asyncio.wait_for(result_future, timeout=timeout)
        logger.bind(tag=TAG).info(
            f"MCP access point tool call {actual_name} successful, original result: {raw_result}"
        )

        if isinstance(raw_result, dict):
            if raw_result.get("isError") is True:
                error_msg = raw_result.get(
                    "error", "Tool call returns error, but no specific error information is provided"
                )
                raise RuntimeError(f"Tool call error: {error_msg}")

            content = raw_result.get("content")
            if isinstance(content, list) and len(content) > 0:
                if isinstance(content[0], dict) and "text" in content[0]:
                    # Return text content directly without JSON parsing
                    return content[0]["text"]
        # If the result is not in the expected format, convert it to a string
        return str(raw_result)
    except asyncio.TimeoutError:
        await mcp_client.cleanup_call_result(tool_call_id)
        raise TimeoutError("Tool call request timeout")
    except Exception as e:
        await mcp_client.cleanup_call_result(tool_call_id)
        raise e
