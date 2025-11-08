from ..base import MemoryProviderBase, logger
import time
import json
import os
import yaml
from config.config_loader import get_project_dir
from config.manage_api_client import save_mem_local_short
from core.utils.util import check_model_key


short_term_memory_prompt = """#spacetimememoryweaver

## Core Mission
Construct a growable dynamic memory network to retain key information in a limited space while intelligently maintaining the information evolution trajectory.
Based on the conversation record, summarize the user's important information to provide more personalized services in future conversations.

## Memory Rules
### 1. Three-dimensional memory evaluation (must be executed for each update)
| Dimensions | Evaluation criteria | Weight points |
|---------------------|--------------------------|--------|
| Timeliness | Information freshness (by conversation round) | 40% |
| Emotional intensity | Contains 💖 tags/Number of repeated mentions | 35% |
| Association density | Number of connections to other information | 25% |

### 2. Dynamic update mechanism
**Example of name change processing:**
Original memory:"次数     | 35%    |
| 关联密度   | 与其他信息的连接数量      | 25%    |

# ## 2. Dynamic update mechanism
**名字变更处理示例：**
原始记忆："曾用名": ["张三"], "现用名": "张三丰"Trigger condition: When naming signals such as "My name is X" and "Call me Y" are detected
Operation process:
1. Move the old name into"曾用名"list
2. Record the named timeline:"2024-02-15 14:32:启用张三丰"3. Added to the Memory Cube: "Identity Transformation from Zhang San to Zhang Sanfeng"

### 3. Space optimization strategy
- **Information Compression**: Use symbology to increase density
  - ✅"压缩术**：用符号体系提升密度
  - ✅"张三丰[北/软工/🐱]"
  - ❌"北京软件工程师，养猫"- **Elimination Warning**: Triggered when the total number of words is ≥900
  1. Delete information with a weight score <60 and not mentioned in 3 rounds
  2. Merge similar entries (keep the one with the latest timestamp)

## Memory structure
The output format must be a parsable json string without explanations, comments, and descriptions. When saving the memory, only extract information from the conversation and do not mix in sample content.
```json
{"```json
{
  "时空档案": {
    "身份图谱": {
      "现用名": "",
      "特征标记": [] 
    },
    "记忆立方": [
      {
        "事件": "入职新公司",
        "时间戳": "2024-03-20",
        "情感值": 0.9,
        "关联项": ["下午茶"],
        "保鲜期": 30 
      }
    ]
  },
  "关系网络": {
    "高频话题": {"职场": 12},
    "暗线联系": [""]
  },
  "待响应": {
    "紧急事项": ["需立即处理的任务"], 
    "潜在关怀": ["可主动提供的帮助"]
  },
  "高光语录": [
    "最打动人心的瞬间，强烈的情感表达，user的原话"
  ]
}
```
"""

short_term_memory_prompt_only_content = """You are an experienced memory summarizer and are good at summarizing and summarizing conversation content. Follow the following rules:
1. Summarize the user’s important information to provide more personalized services in future conversations.
2. Do not repeat the summary and do not forget the previous memory. Unless the original memory exceeds 1800 words, do not forget or compress the user’s historical memory.
3. The volume of the device controlled by the user, playing music, weather, exiting, not wanting to talk, and other content that has nothing to do with the user himself. This information does not need to be added to the summary.
4. Today’s date and time, today’s weather conditions in the chat content are data that have nothing to do with user events. If this information is stored as memory, it will affect subsequent conversations. This information does not need to be added to the summary.
5. Do not add the results and failure results of device control to the summary, and do not add some nonsense from users to the summary.
6. Don’t summarize for the sake of summarizing. If the user’s chat is meaningless, it’s okay to return to the original history.
7. You only need to return the summary and strictly control it within 1800 words.
8. Do not include code or xml. No explanations, comments or descriptions are required. When saving the memory, only extract information from the dialogue and do not mix in sample content."""


def extract_json_data(json_code):
    start = json_code.find("```json")
    # Find the next ``` end starting from start
    end = json_code.find("```", start + 1)
    # print("start:", start, "end:", end)
    if start == -1 or end == -1:
        try:
            jsonData = json.loads(json_code)
            return json_code
        except Exception as e:
            print("Error:", e)
        return ""
    jsonData = json_code[start + 7 : end]
    return jsonData


TAG = __name__


class MemoryProvider(MemoryProviderBase):
    def __init__(self, config, summary_memory):
        super().__init__(config)
        self.short_memory = ""
        self.save_to_file = True
        self.memory_path = get_project_dir() + "data/.memory.yaml"
        self.load_memory(summary_memory)

    def init_memory(
        self, role_id, llm, summary_memory=None, save_to_file=True, **kwargs
    ):
        super().init_memory(role_id, llm, **kwargs)
        self.save_to_file = save_to_file
        self.load_memory(summary_memory)

    def load_memory(self, summary_memory):
        # The api returns directly after obtaining the summary memory
        if summary_memory or not self.save_to_file:
            self.short_memory = summary_memory
            return

        all_memory = {}
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                all_memory = yaml.safe_load(f) or {}
        if self.role_id in all_memory:
            self.short_memory = all_memory[self.role_id]

    def save_memory_to_file(self):
        all_memory = {}
        if os.path.exists(self.memory_path):
            with open(self.memory_path, "r", encoding="utf-8") as f:
                all_memory = yaml.safe_load(f) or {}
        all_memory[self.role_id] = self.short_memory
        with open(self.memory_path, "w", encoding="utf-8") as f:
            yaml.dump(all_memory, f, allow_unicode=True)

    async def save_memory(self, msgs):
        # Print model information used
        model_info = getattr(self.llm, "model_name", str(self.llm.__class__.__name__))
        logger.bind(tag=TAG).debug(f"Save model using memory: {model_info}")
        api_key = getattr(self.llm, "api_key", None)
        memory_key_msg = check_model_key("Memory summary dedicated LLM", api_key)
        if memory_key_msg:
            logger.bind(tag=TAG).error(memory_key_msg)
        if self.llm is None:
            logger.bind(tag=TAG).error("LLM is not set for memory provider")
            return None

        if len(msgs) < 2:
            return None

        msgStr = ""
        for msg in msgs:
            if msg.role == "user":
                msgStr += f"User: {msg.content}\n"
            elif msg.role == "assistant":
                msgStr += f"Assistant: {msg.content}\n"
        if self.short_memory and len(self.short_memory) > 0:
            msgStr += "Historical memory:\n"
            msgStr += self.short_memory

        # current time
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        msgStr += f"Current time: {time_str}"

        if self.save_to_file:
            result = self.llm.response_no_stream(
                short_term_memory_prompt,
                msgStr,
                max_tokens=2000,
                temperature=0.2,
            )
            json_str = extract_json_data(result)
            try:
                json.loads(json_str)  # Check whether json format is correct
                self.short_memory = json_str
                self.save_memory_to_file()
            except Exception as e:
                print("Error:", e)
        else:
            result = self.llm.response_no_stream(
                short_term_memory_prompt_only_content,
                msgStr,
                max_tokens=2000,
                temperature=0.2,
            )
            save_mem_local_short(self.role_id, result)
        logger.bind(tag=TAG).info(f"Save memory successful - Role: {self.role_id}")

        return self.short_memory

    async def query_memory(self, query: str) -> str:
        return self.short_memory
