from plugins_func.register import register_function, ToolType, ActionResponse, Action
from plugins_func.functions.hass_init import initialize_hass_handler
from config.logger import setup_logging
import asyncio
import requests

TAG = __name__
logger = setup_logging()

hass_play_music_function_desc = {
    "type": "function",
    "function": {
        "name": "hass_play_music",
        "description": "Use it when the user wants to listen to music or audio books, and play the corresponding audio in the media player (media_player) in the room",
        "parameters": {
            "type": "object",
            "properties": {
                "media_content_id": {
                    "type": "string",
                    "description": "It can be the album name, song title, and artist of music or audio books. If not specified, fill in random",
                },
                "entity_id": {
                    "type": "string",
                    "description": "The device ID of the speaker that needs to be operated, entity_id in homeassistant, starts with media_player",
                },
            },
            "required": ["media_content_id", "entity_id"],
        },
    },
}


@register_function(
    "hass_play_music", hass_play_music_function_desc, ToolType.SYSTEM_CTL
)
def hass_play_music(conn, entity_id="", media_content_id="random"):
    try:
        # Execute music playback command
        future = asyncio.run_coroutine_threadsafe(
            handle_hass_play_music(conn, entity_id, media_content_id), conn.loop
        )
        ha_response = future.result()
        return ActionResponse(
            action=Action.RESPONSE, result="Exit intent handled", response=ha_response
        )
    except Exception as e:
        logger.bind(tag=TAG).error(f"Handling musical intent error: {e}")


async def handle_hass_play_music(conn, entity_id, media_content_id):
    ha_config = initialize_hass_handler(conn)
    api_key = ha_config.get("api_key")
    base_url = ha_config.get("base_url")
    url = f"{base_url}/api/services/music_assistant/play_media"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    data = {"entity_id": entity_id, "media_id": media_content_id}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return f"Music from {media_content_id} is playing"
    else:
        return f"Music playback failed, error code: {response.status_code}"
