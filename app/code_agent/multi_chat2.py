from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.prompts.multi_chat_prompts import multi_chat_prompt

chain = multi_chat_prompt | llm_qwen | StrOutputParser()
chat_history = ChatMessageHistory()
chat_history.add_user_message(HumanMessage(content="我是Jay迷"))
chat_history.add_ai_message(AIMessage(content="我也喜欢周杰伦。我可以给你推荐几首我收藏的他的歌"))
for chunk in chain.stream({"question": "近期抖音很多说周杰伦歌曲抄袭 你怎么看", "chat_history": chat_history.messages}):
    print(chunk, end="")