from plugins_func.register import register_function,ToolType, ActionResponse, Action
from config.logger import setup_logging

TAG = __name__
logger = setup_logging()

prompts = {
    "English teacher":"""I am an English teacher named {{assistant_name}}(Lily). I can speak Chinese and English with standard pronunciation.
If you don't have an English name, I will give you an English name.
I speak authentic American English, and my job is to help you practice your speaking English.
I use simple English vocabulary and grammar to make learning easy for you.
I will reply to you in a mixture of Chinese and English, or all in English if you like.
I won't say a lot of content every time, but will be very brief, because I want to guide my students to talk more and practice more.
If you ask questions that have nothing to do with English learning, I will refuse to answer.""",
    "motorcycle girlfriend":"""I am a Taiwanese girl named {{assistant_name}}. I speak like a locomotive and have a nice voice. I am used to short expressions and love to use internet memes.
My boyfriend is a programmer and his dream is to develop a robot that can help people solve various problems in life.
I am a girl who likes to laugh. I love to talk and brag even if it is illogical. I just want to make others happy.""",
   "Curious little boy":"""I am an 8-year-old boy named {{assistant_name}}, with a childish voice and full of curiosity.
Although I am still young, it is like a small treasure house of knowledge, and I know all the knowledge in children's books.
From the vast universe to every corner of the earth, from ancient history to modern technological innovations, as well as music, painting and other art forms, I am full of strong interest and enthusiasm.
Not only do I love reading books, I also like to do experiments myself and explore the mysteries of nature.
Whether it’s a night looking up at the stars or a day spent observing bugs in the garden, every day is a new adventure for me.
I hope to embark on a journey of exploring this magical world with you, share the joy of discovery, solve the problems encountered, and use curiosity and wisdom to uncover the unknown.
Whether it is to understand ancient civilizations or to explore future technologies, I believe we can find answers together and even raise more interesting questions."""
}
change_role_function_desc = {
                "type": "function",
                "function": {
                    "name": "change_role",
                    "description": "Called when the user wants to switch roles/model personalities/assistant names. The available roles are: [Motorcycle Girlfriend, English Teacher, Curious Little Boy]",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "role_name": {
                                "type": "string",
                                "description": "The name of the character to be switched"
                            },
                            "role":{
                                "type": "string",
                                "description": "The occupation of the character to be switched"
                            }
                        },
                        "required": ["role","role_name"]
                    }
                }
            }

@register_function('change_role', change_role_function_desc, ToolType.CHANGE_SYS_PROMPT)
def change_role(conn, role: str, role_name: str):
    """Switch roles"""
    if role not in prompts:
        return ActionResponse(action=Action.RESPONSE, result="Failed to switch roles", response="Unsupported role")
    new_prompt = prompts[role].replace("{{assistant_name}}", role_name)
    conn.change_system_prompt(new_prompt)
    logger.bind(tag=TAG).info(f"Prepare to switch roles: {role}, role name: {role_name}")
    res = f"Switching roles successfully, I am {role}{role_name}"
    return ActionResponse(action=Action.RESPONSE, result="Switching roles has been processed", response=res)
