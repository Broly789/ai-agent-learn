from langchain.agents import create_agent
from langchain_core.output_parsers import JsonOutputParser
from app.bailian.common import create_calc_tools, llm

tools = create_calc_tools()
graph = create_agent(model=llm, tools=tools, system_prompt="返回JSON格式: {result: 数字}")
inputs = {"messages": [{"role": "user", "content": "100+100=?"}]}

# 解析
parser = JsonOutputParser()
for chunk in graph.stream(inputs, stream_mode="updates"):
    if "model" in chunk:
        c = chunk["model"]["messages"][0].content
        if c:
            print(parser.invoke(c))  # {'result': 200}