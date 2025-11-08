from abc import ABC, abstractmethod
from typing import List, Dict
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()


class IntentProviderBase(ABC):
    def __init__(self, config):
        self.config = config

    def set_llm(self, llm):
        self.llm = llm
        # Get model name and type information
        model_name = getattr(llm, "model_name", str(llm.__class__.__name__))
        # Keep more detailed logs
        logger.bind(tag=TAG).info(f"Intent recognition settings LLM: {model_name}")

    @abstractmethod
    async def detect_intent(self, conn, dialogue_history: List[Dict], text: str) -> str:
        """Detect the intent of the user’s last sentence
        Args:
            dialogue_history: dialogue history list, each record contains role and content
        Returns:
            Returns the recognized intent in the format:
            -"继续聊天"
            - "结束聊天"
            - "播放音乐 歌名"or"随机播放音乐"
            - "查询天气 地点名"or"查询天气 [当前位置]"
        """
        pass
