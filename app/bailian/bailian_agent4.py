from langchain.agents import create_agent
from app.bailian.common import create_calc_tools, llm, chat_prompt_template
import json

tools = create_calc_tools()

graph = create_agent(
    model=llm,
    tools=tools,
    system_prompt="你是数学助手。请以 JSON 格式返回：{\"args\": \"算式\", \"result\": 数字}"
)

# 使用 chat_prompt_template 生成消息
messages = chat_prompt_template.format_messages(
    role="数学",
    something="100+100=?"
)

result = graph.invoke({"messages": messages})
output = json.loads(result["messages"][-1].content)

print(f"工具入参: {output['args']}")
print(f"计算结果: {output['result']}")
