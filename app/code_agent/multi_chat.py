import uuid
from idlelib.run import get_message_lines
from langchain.agents import create_agent
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory, FileChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.prompts.multi_chat_prompts import multi_chat_prompt


def get_message_history(session_id:  str):
    return FileChatMessageHistory(f"{session_id}.json")

file_toolkit = FileManagementToolkit(root_dir="/Users/brolylee/2026web/ai-agent/.temp")
file_tools = file_toolkit.get_tools()

agent = create_agent(
    model=llm_qwen,
    tools=file_tools,
    system_prompt="你是一个智能助手，你可以读取文件内容并根据文件内容回答问题。",
)

chain = multi_chat_prompt | agent
chain_with_history = RunnableWithMessageHistory(
    runnable=chain,
    get_session_history= get_message_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)
# chat_history = ChatMessageHistory()
# chat_history.add_user_message(HumanMessage(content="我是Jay迷"))
# chat_history.add_ai_message(AIMessage(content="我也喜欢周杰伦。我可以给你推荐几首我收藏的他的歌"))
# for chunk in chain.stream({"question": "近期抖音很多说周杰伦歌曲抄袭 你怎么看", "chat_history": []}):
#     print(chunk, end="")

session_id = uuid.uuid4()

while True:
    user_input = input("用户：")
    if user_input.lower() == "exit":
        break
    print("助手：", end="")
    for chunk in chain_with_history.stream({"question": user_input}, config={"configurable": {"session_id": str(session_id)}}):
        print(chunk, end="")

    print("\n")
