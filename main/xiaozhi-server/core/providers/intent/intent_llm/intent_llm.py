from typing import List, Dict
from ..base import IntentProviderBase
from plugins_func.functions.play_music import initialize_music_handler
from config.logger import setup_logging
import re
import json
import hashlib
import time

TAG = __name__
logger = setup_logging()


class IntentProvider(IntentProviderBase):
    def __init__(self, config):
        super().__init__(config)
        self.llm = None
        self.promot = ""
        # Import global cache manager
        from core.utils.cache.manager import cache_manager, CacheType

        self.cache_manager = cache_manager
        self.CacheType = CacheType
        self.history_count = 4  # By default, the last 4 conversation records are used

    def get_intent_system_prompt(self, functions_list: str) -> str:
        """Dynamically generate system prompt words based on configured intent options and available functions
        Args:
            functions: list of available functions, JSON format string
        Returns:
            Formatted system prompt words"""

        # Build function description section
        functions_desc = "List of available functions:\n"
        for func in functions_list:
            func_info = func.get("function", {})
            name = func_info.get("name", "")
            desc = func_info.get("description", "")
            params = func_info.get("parameters", {})

            functions_desc += f"\nFunction name: {name}\n"
            functions_desc += f"Description: {desc}\n"

            if params:
                functions_desc += "Parameters:\n"
                for param_name, param_info in params.get("properties", {}).items():
                    param_desc = param_info.get("description", "")
                    param_type = param_info.get("type", "")
                    functions_desc += f"- {param_name} ({param_type}): {param_desc}\n"

            functions_desc += "---\n"

        prompt = (
            "[Strict format requirements] You must only return JSON format, and absolutely cannot return any natural language! \n\n"
            "You are an intent recognition assistant. Please analyze the user's last sentence, determine the user's intention and call the corresponding function. \n\n"

            "[Important Rules] For the following types of queries, please return result_for_context directly without calling the function:\n"
            "- Ask for the current time (such as: what time is it now, current time, query time, etc.)\n"
            "- Ask for today's date (such as: today's date, today's day of the week, today's date, etc.)\n"
            "- Ask about today's lunar calendar (such as: what's the lunar date today, what's the solar term today, etc.)\n"
            "- Ask about the city (such as: where am I now, do you know which city I am in, etc.)"
            "Answers are constructed directly from contextual information. \n\n"
            "- If the user uses question words (such as 'how', 'why', 'how') to ask exit-related questions (such as 'How did you exit?'), please note that this does not allow you to exit, please return {'function_call': {'name': 'continue_chat'}\n"
            "- handle_exit_intent\n\n is only triggered when the user explicitly uses commands such as 'Exit the system', 'End conversation', 'I don't want to talk to you anymore', etc."
            f"{functions_desc}\n"
            "Processing steps:\n"
            "1. Analyze user input and determine user intent\n"
            "2. Check whether it is the above basic information query (time, date, etc.), if so, return result_for_context\n"
            "3. Select the best matching function from the list of available functions\n"
            "4. If a matching function is found, generate the corresponding function_call format\n"
            '5. 如果没有找到匹配的函数，返回{"function_call": {"name": "continue_chat"}}\n\n'
            "Return format requirements:\n"
            "1. Must return pure JSON format, do not contain any other text\n"
            "2. Must contain function_call field\n"
            "3. function_call must contain the name field\n"
            "4. If the function requires parameters, the arguments field must be included\n\n"
            "Example:\n"
            "```\n"
            "User: What time is it now? \n"
            '返回: {"function_call": {"name": "result_for_context"}}\n'
            "```\n"
            "```\n"
            "User: What is the current battery level? \n"
            '返回: {"function_call": {"name": "get_battery_level", "arguments": {"response_success": "The current battery level is {value}%", "response_failure": "Unable to obtain the current battery percentage of the Battery"}}}\n'
            "```\n"
            "```\n"
            "User: What is the current screen brightness? \n"
            '返回: {"function_call": {"name": "self_screen_get_brightness"}}\n'
            "```\n"
            "```\n"
            "User: Set screen brightness to 50%\n"
            '返回: {"function_call": {"name": "self_screen_set_brightness", "arguments": {"brightness": 50}}}\n'
            "```\n"
            "```\n"
            "User: I want to end the conversation\n"
            '返回: {"function_call": {"name": "handle_exit_intent", "arguments": {"say_goodbye": "goodbye"}}}\n'
            "```\n"
            "```\n"
            "User: Hello\n"
            '返回: {"function_call": {"name": "continue_chat"}}\n'
            "```\n\n"
            "Note:\n"
            "1. Only return JSON format, do not include any other text\n"
            '2. 优先检查用户查询是否为基础信息（时间、日期等），如是则返回{"function_call": {"name": "result_for_context"}}，不需要arguments参数\n'
            '3. 如果没有找到匹配的函数，返回{"function_call": {"name": "continue_chat"}}\n'
            "4. Make sure the returned JSON is in the correct format and contains all necessary fields\n"
            "5. result_for_context does not require any parameters, the system will automatically obtain information from the context\n"
            "Special instructions:\n"
            "- When the user inputs multiple commands in a single input (such as 'turn on the lights and turn up the volume')\n"
            "- Please return a JSON array composed of multiple function_calls\n"
            "- Example: {'function_calls': [{name:'light_on'}, {name:'volume_up'}]}\n\n"
            "[Final Warning] It is absolutely forbidden to output any natural language, emoticons or explanatory text! Only valid JSON format can be output! Violation of this rule will result in system errors!"
        )
        return prompt

    def replyResult(self, text: str, original_text: str):
        llm_result = self.llm.response_no_stream(
            system_prompt=text,
            user_prompt="Please reply to the user based on the above content and speak like a human being. Please be concise and please return the results directly. Users are now saying:"
            + original_text,
        )
        return llm_result

    async def detect_intent(self, conn, dialogue_history: List[Dict], text: str) -> str:
        if not self.llm:
            raise ValueError("LLM provider not set")
        if conn.func_handler is None:
            return '{"function_call": {"name": "continue_chat"}}'

        # Record overall start time
        total_start_time = time.time()

        # Print model information used
        model_info = getattr(self.llm, "model_name", str(self.llm.__class__.__name__))
        logger.bind(tag=TAG).debug(f"Use the intent recognition model: {model_info}")

        # Calculate cache key
        cache_key = hashlib.md5((conn.device_id + text).encode()).hexdigest()

        # Check cache
        cached_intent = self.cache_manager.get(self.CacheType.INTENT, cache_key)
        if cached_intent is not None:
            cache_time = time.time() - total_start_time
            logger.bind(tag=TAG).debug(
                f"Intent to use cache: {cache_key} -> {cached_intent}, time taken: {cache_time:.4f} seconds"
            )
            return cached_intent

        if self.promot == "":
            functions = conn.func_handler.get_functions()
            if hasattr(conn, "mcp_client"):
                mcp_tools = conn.mcp_client.get_available_tools()
                if mcp_tools is not None and len(mcp_tools) > 0:
                    if functions is None:
                        functions = []
                    functions.extend(mcp_tools)

            self.promot = self.get_intent_system_prompt(functions)

        music_config = initialize_music_handler(conn)
        music_file_names = music_config["music_file_names"]
        prompt_music = f"{self.promot}\n<musicNames>{music_file_names}\n</musicNames>"

        home_assistant_cfg = conn.config["plugins"].get("home_assistant")
        if home_assistant_cfg:
            devices = home_assistant_cfg.get("devices", [])
        else:
            devices = []
        if len(devices) > 0:
            hass_prompt = "\nThe following is a list of my smart devices (location, device name, entity_id), which can be controlled through homeassistant\n"
            for device in devices:
                hass_prompt += device + "\n"
            prompt_music += hass_prompt

        logger.bind(tag=TAG).debug(f"User prompt: {prompt_music}")

        # Tips for building user conversation history
        msgStr = ""

        # Get recent conversation history
        start_idx = max(0, len(dialogue_history) - self.history_count)
        for i in range(start_idx, len(dialogue_history)):
            msgStr += f"{dialogue_history[i].role}: {dialogue_history[i].content}\n"

        msgStr += f"User: {text}\n"
        user_prompt = f"current dialogue:\n{msgStr}"

        # Record preprocessing completion time
        preprocess_time = time.time() - total_start_time
        logger.bind(tag=TAG).debug(f"Intent recognition preprocessing takes: {preprocess_time:.4f} seconds")

        # Using LLM for intent recognition
        llm_start_time = time.time()
        logger.bind(tag=TAG).debug(f"Start LLM intent recognition call, model: {model_info}")

        intent = self.llm.response_no_stream(
            system_prompt=prompt_music, user_prompt=user_prompt
        )

        # Record LLM call completion time
        llm_time = time.time() - llm_start_time
        logger.bind(tag=TAG).debug(
            f"LLM intent recognition completed, model: {model_info}, call time: {llm_time:.4f} seconds"
        )

        # Record post-processing start time
        postprocess_start_time = time.time()

        # Clean and parse responses
        intent = intent.strip()
        # Try to extract the JSON part
        match = re.search(r"\{.*\}", intent, re.DOTALL)
        if match:
            intent = match.group(0)

        # Record total processing time
        total_time = time.time() - total_start_time
        logger.bind(tag=TAG).debug(
            f"[Intent recognition performance] Model: {model_info}, total time taken: {total_time:.4f} seconds, LLM call: {llm_time:.4f} seconds, query: '{text[:20]}...'"
        )

        # Try parsing to JSON
        try:
            intent_data = json.loads(intent)
            # If function_call is included, format it into a format suitable for processing
            if "function_call" in intent_data:
                function_data = intent_data["function_call"]
                function_name = function_data.get("name")
                function_args = function_data.get("arguments", {})

                # Record the recognized function call
                logger.bind(tag=TAG).info(
                    f"llm recognized intent: {function_name}, parameters: {function_args}"
                )

                # Handle different types of intents
                if function_name == "result_for_context":
                    # Process basic information queries and build results directly from context
                    logger.bind(tag=TAG).info("result_for_context intent detected, will answer directly using context information")
                    
                elif function_name == "continue_chat":
                    # Handle normal conversations
                    # Keep non-tool related messages
                    clean_history = [
                        msg
                        for msg in conn.dialogue.dialogue
                        if msg.role not in ["tool", "function"]
                    ]
                    conn.dialogue.dialogue = clean_history
                    
                else:
                    # Handle function calls
                    logger.bind(tag=TAG).info(f"Function call intent detected: {function_name}")

            # Unified cache handling and returns
            self.cache_manager.set(self.CacheType.INTENT, cache_key, intent)
            postprocess_time = time.time() - postprocess_start_time
            logger.bind(tag=TAG).debug(f"Intent post-processing time: {postprocess_time:.4f} seconds")
            return intent
        except json.JSONDecodeError:
            # post processing time
            postprocess_time = time.time() - postprocess_start_time
            logger.bind(tag=TAG).error(
                f"Unable to parse intent JSON: {intent}, post-processing time: {postprocess_time:.4f} seconds"
            )
            # If the parsing fails, the default intention to continue chatting is returned.
            return '{"function_call": {"name": "continue_chat"}}'
