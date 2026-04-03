from langchain.agents import create_agent
from app.bailian.common import create_calc_tools, llm

# 你的工具
tools = create_calc_tools()

# 创建智能体（一行搞定）
graph = create_agent(llm, tools)



inputs = {"messages": [{"role": "user", "content": "100+100=?"}]}
full_response = []

for chunk in graph.stream(inputs, stream_mode="updates"):
    # 只提取 model 产生的消息
    if "model" in chunk:
        msg = chunk["model"]["messages"][0]
        # 只要有内容就收集
        if msg.content:
            full_response.append(msg.content)

# 最后一条就是最终答案！
final_answer = full_response[-1]
print("最终结果：", final_answer)
