from langchain_core.messages import HumanMessage
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig

from app.code_agent.tools.file_tools import file_tools
from app.code_agent.model.qwen import llm_qwen
from langgraph.checkpoint.redis import RedisSaver

# 👇 真正稳定、不报错、纯Redis持久化
# 启动Redis Stack
# docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack-server:latest


# 提示词（必须加）
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个智能助手，可以回答用户问题。"),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

def create_ai_agent():
    with RedisSaver.from_conn_string("redis://127.0.0.1:6379") as memory:
        # 创建必要的索引
        memory.setup()
        agent = create_agent(
            model=llm_qwen,
            tools=file_tools,
            system_prompt="你是一个智能助手,你可以回答用户的问题。",
            checkpointer=memory,
            debug=True,
        )
        return agent

# ==========================
# 测试（永久记忆）
# ==========================
if __name__ == "__main__":
    config = RunnableConfig(configurable={"thread_id": 1})
    agent = create_ai_agent()
    # res = agent.invoke(input={"messages": [HumanMessage(content="我叫Broly,我喜欢龙珠布罗利")]}, config=config)
    # print(res)
    # print("="*50)
    res = agent.invoke(input={"messages": [HumanMessage(content="我叫什么名字 YIYI一句话告诉我")]}, config=config)
    print("="*50)
    print(res)
