import uuid
from idlelib.run import get_message_lines

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables import RunnableWithMessageHistory

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.prompts.multi_chat_prompts import multi_chat_prompt
store = {}
def get_message_history(session_id:  str):
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
        print(store)
    return store[session_id]

chain = multi_chat_prompt | llm_qwen | StrOutputParser()
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
print(session_id)

while True:
    user_input = input("用户：")
    if user_input.lower() == "exit":
        break
    response = chain_with_history.invoke({"question": user_input}, config={"configurable": {"session_id": str(session_id)}})
    print("助手：", end="")
    for chunk in response:
        print(chunk, end="")

    print("\n")
