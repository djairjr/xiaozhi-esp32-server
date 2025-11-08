from plugins_func.register import register_function, ToolType, ActionResponse, Action
from plugins_func.functions.hass_init import initialize_hass_handler
from config.logger import setup_logging
import asyncio
import requests

TAG = __name__
logger = setup_logging()

hass_set_state_function_desc = {
    "type": "function",
    "function": {
        "name": "hass_set_state",
        "description": "Set the status of the device in HomeAssistant, including turning it on and off, adjusting the brightness, color, and color temperature of the light, adjusting the volume of the player, and pausing, continuing, and muting the device.",
        "parameters": {
            "type": "object",
            "properties": {
                "state": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "Actions that require operation, turn on the device: turn_on, turn off the device: turn_off, increase brightness: brightness_up, decrease brightness: brightness_down, set brightness: brightness_value, increase volume: volume_up, decrease volume: volume_down, set volume: volume_set, set color temperature: set_kelvin, set color: set_color, device pause: pause, device continue: continue, mute/unmute: volume_mute",
                        },
                        "input": {
                            "type": "integer",
                            "description": "It is only needed when setting the volume and brightness. The valid value is 1-100, corresponding to 1%-100% of the volume and brightness.",
                        },
                        "is_muted": {
                            "type": "string",
                            "description": "It is only required when setting the mute operation. When setting the mute, the value is true, and when canceling the mute, the value is false.",
                        },
                        "rgb_color": {
                            "type": "array",
                            "items": {"type": "integer"},
                            "description": "It is only needed when setting the color. Fill in the RGB value of the target color here.",
                        },
                    },
                    "required": ["type"],
                },
                "entity_id": {
                    "type": "string",
                    "description": "The device ID that needs to be operated, the entity_id in homeassistant",
                },
            },
            "required": ["state", "entity_id"],
        },
    },
}


@register_function("hass_set_state", hass_set_state_function_desc, ToolType.SYSTEM_CTL)
def hass_set_state(conn, entity_id="", state=None):
    if state is None:
        state = {}
    try:
        ha_response = handle_hass_set_state(conn, entity_id, state)
        return ActionResponse(Action.REQLLM, ha_response, None)
    except asyncio.TimeoutError:
        logger.bind(tag=TAG).error("Set Home Assistant status timeout")
        return ActionResponse(Action.ERROR, "Request timeout", None)
    except Exception as e:
        error_msg = f"Failed to perform Home Assistant operation"
        logger.bind(tag=TAG).error(error_msg)
        return ActionResponse(Action.ERROR, error_msg, None)


def handle_hass_set_state(conn, entity_id, state):
    ha_config = initialize_hass_handler(conn)
    api_key = ha_config.get("api_key")
    base_url = ha_config.get("base_url")
    """
    state = { "type":"brightness_up","input":"80","is_muted":"true"}
    """
    domains = entity_id.split(".")
    if len(domains) > 1:
        domain = domains[0]
    else:
        return "Execution failed, wrong device id"
    action = ""
    arg = ""
    value = ""
    if state["type"] == "turn_on":
        description = "Device is on"
        if domain == "cover":
            action = "open_cover"
        elif domain == "vacuum":
            action = "start"
        else:
            action = "turn_on"
    elif state["type"] == "turn_off":
        description = "Device is turned off"
        if domain == "cover":
            action = "close_cover"
        elif domain == "vacuum":
            action = "stop"
        else:
            action = "turn_off"
    elif state["type"] == "brightness_up":
        description = "The lights have been turned up"
        action = "turn_on"
        arg = "brightness_step_pct"
        value = 10
    elif state["type"] == "brightness_down":
        description = "lights dimmed"
        action = "turn_on"
        arg = "brightness_step_pct"
        value = -10
    elif state["type"] == "brightness_value":
        description = f"Brightness adjusted to {state['input']}"
        action = "turn_on"
        arg = "brightness_pct"
        value = state["input"]
    elif state["type"] == "set_color":
        description = f"Color adjusted to {state['rgb_color']}"
        action = "turn_on"
        arg = "rgb_color"
        value = state["rgb_color"]
    elif state["type"] == "set_kelvin":
        description = f"Color temperature has been adjusted to {state['input']}K"
        action = "turn_on"
        arg = "kelvin"
        value = state["input"]
    elif state["type"] == "volume_up":
        description = "Volume is turned up"
        action = state["type"]
    elif state["type"] == "volume_down":
        description = "Volume has been turned down"
        action = state["type"]
    elif state["type"] == "volume_set":
        description = f"Volume has been adjusted to {state['input']}"
        action = state["type"]
        arg = "volume_level"
        value = state["input"]
        if state["input"] >= 1:
            value = state["input"] / 100
    elif state["type"] == "volume_mute":
        description = f"Device is muted"
        action = state["type"]
        arg = "is_volume_muted"
        value = state["is_muted"]
    elif state["type"] == "pause":
        description = f"Device is paused"
        action = state["type"]
        if domain == "media_player":
            action = "media_pause"
        if domain == "cover":
            action = "stop_cover"
        if domain == "vacuum":
            action = "pause"
    elif state["type"] == "continue":
        description = f"The device has been continued"
        if domain == "media_player":
            action = "media_play"
        if domain == "vacuum":
            action = "start"
    else:
        return f"{domain} {state['type']} functionality is not supported yet"

    if arg == "":
        data = {
            "entity_id": entity_id,
        }
    else:
        data = {"entity_id": entity_id, arg: value}
    url = f"{base_url}/api/services/{domain}/{action}"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data, timeout=5)  # Set a 5 second timeout
    logger.bind(tag=TAG).info(
        f"Set status:{description},url:{url},return_code:{response.status_code}"
    )
    if response.status_code == 200:
        return description
    else:
        return f"Setting failed, error code: {response.status_code}"
