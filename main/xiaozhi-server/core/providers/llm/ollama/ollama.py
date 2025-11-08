from config.logger import setup_logging
from openai import OpenAI
import json
from core.providers.llm.base import LLMProviderBase

TAG = __name__
logger = setup_logging()


class LLMProvider(LLMProviderBase):
    def __init__(self, config):
        self.model_name = config.get("model_name")
        self.base_url = config.get("base_url", "http://localhost:11434")
        # Initialize OpenAI client with Ollama base URL
        # If there is no v1, add v1
        if not self.base_url.endswith("/v1"):
            self.base_url = f"{self.base_url}/v1"

        self.client = OpenAI(
            base_url=self.base_url,
            api_key="ollama",  # Ollama doesn't need an API key but OpenAI client requires one
        )

        # Check if it is a qwen3 model
        self.is_qwen3 = self.model_name and self.model_name.lower().startswith("qwen3")

    def response(self, session_id, dialogue, **kwargs):
        try:
            # If it is a qwen3 model, add the /no_think directive to the user’s last message
            if self.is_qwen3:
                # Copy the conversation list to avoid modifying the original conversation
                dialogue_copy = dialogue.copy()

                # Find the last user message
                for i in range(len(dialogue_copy) - 1, -1, -1):
                    if dialogue_copy[i]["role"] == "user":
                        # Add /no_think directive before user message
                        dialogue_copy[i]["content"] = (
                            "/no_think " + dialogue_copy[i]["content"]
                        )
                        logger.bind(tag=TAG).debug(f"Add /no_think directive for qwen3 model")
                        break

                # Use modified dialogue
                dialogue = dialogue_copy

            responses = self.client.chat.completions.create(
                model=self.model_name, messages=dialogue, stream=True
            )
            is_active = True
            # Used to handle cross-chunk tags
            buffer = ""

            for chunk in responses:
                try:
                    delta = (
                        chunk.choices[0].delta
                        if getattr(chunk, "choices", None)
                        else None
                    )
                    content = delta.content if hasattr(delta, "content") else ""

                    if content:
                        # Add content to buffer
                        buffer += content

                        # Process tags in buffer
                        while "<think>" in buffer and "</think>" in buffer:
                            # Find the complete <think></think> tag and remove it
                            pre = buffer.split("<think>", 1)[0]
                            post = buffer.split("</think>", 1)[1]
                            buffer = pre + post

                        # Handle the case where there is only a start tag
                        if "<think>" in buffer:
                            is_active = False
                            buffer = buffer.split("<think>", 1)[0]

                        # Handle the case where there is only a closing tag
                        if "</think>" in buffer:
                            is_active = True
                            buffer = buffer.split("</think>", 1)[1]

                        # If currently active and the buffer has content, output
                        if is_active and buffer:
                            yield buffer
                            buffer = ""  # Clear buffer

                except Exception as e:
                    logger.bind(tag=TAG).error(f"Error processing chunk: {e}")

        except Exception as e:
            logger.bind(tag=TAG).error(f"Error in Ollama response generation: {e}")
            yield "[Ollama service response abnormality]"

    def response_with_functions(self, session_id, dialogue, functions=None):
        try:
            # If it is a qwen3 model, add the /no_think directive to the user’s last message
            if self.is_qwen3:
                # Copy the conversation list to avoid modifying the original conversation
                dialogue_copy = dialogue.copy()

                # Find the last user message
                for i in range(len(dialogue_copy) - 1, -1, -1):
                    if dialogue_copy[i]["role"] == "user":
                        # Add /no_think directive before user message
                        dialogue_copy[i]["content"] = (
                            "/no_think " + dialogue_copy[i]["content"]
                        )
                        logger.bind(tag=TAG).debug(f"Add /no_think directive for qwen3 model")
                        break

                # Use modified dialogue
                dialogue = dialogue_copy

            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=dialogue,
                stream=True,
                tools=functions,
            )

            is_active = True
            buffer = ""

            for chunk in stream:
                try:
                    delta = (
                        chunk.choices[0].delta
                        if getattr(chunk, "choices", None)
                        else None
                    )
                    content = delta.content if hasattr(delta, "content") else None
                    tool_calls = (
                        delta.tool_calls if hasattr(delta, "tool_calls") else None
                    )

                    # If it is a tool call, pass it directly
                    if tool_calls:
                        yield None, tool_calls
                        continue

                    # Process text content
                    if content:
                        # Add content to buffer
                        buffer += content

                        # Process tags in buffer
                        while "<think>" in buffer and "</think>" in buffer:
                            # Find the complete <think></think> tag and remove it
                            pre = buffer.split("<think>", 1)[0]
                            post = buffer.split("</think>", 1)[1]
                            buffer = pre + post

                        # Handle the case where there is only a start tag
                        if "<think>" in buffer:
                            is_active = False
                            buffer = buffer.split("<think>", 1)[0]

                        # Handle the case where there is only a closing tag
                        if "</think>" in buffer:
                            is_active = True
                            buffer = buffer.split("</think>", 1)[1]

                        # If currently active and the buffer has content, output
                        if is_active and buffer:
                            yield buffer, None
                            buffer = ""  # Clear buffer
                except Exception as e:
                    logger.bind(tag=TAG).error(f"Error processing function chunk: {e}")
                    continue

        except Exception as e:
            logger.bind(tag=TAG).error(f"Error in Ollama function call: {e}")
            yield f"[Ollama service response exception: {str(e)}]", None
