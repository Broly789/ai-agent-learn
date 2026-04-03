import json
from pydantic import BaseModel, Field
from langchain.agents import create_agent
from langchain_core.output_parsers import JsonOutputParser
from app.bailian.common import create_calc_tools, llm, chat_prompt_template

# 1. 定义数据模型，用于约束 LLM 的输出结构
class MathResult(BaseModel):
    args: str = Field(description="原始算式")
    result: float = Field(description="计算出的数字结果")

# 2. 工具和模型准备
tools = create_calc_tools()

# 将 Pydantic 类作为工具绑定，强制模型理解该格式
llm_with_tools = llm.bind_tools(tools + [MathResult])

# 3. 创建智能体
graph = create_agent(
    model=llm_with_tools,
    tools=tools,
    system_prompt=(
        "你是数学助手。请通过计算工具解决问题。"
        "最终请返回符合以下格式的 JSON："
        "{\"args\": \"算式\", \"result\": 数字}"
    )
)

# 4. 准备消息
messages = chat_prompt_template.format_messages(
    role="数学",
    something="100+100=?"
)

# 5. 执行调用
result = graph.invoke({"messages": messages})
content = result["messages"][-1].content

# 6. 使用 JsonOutputParser 稳健解析输出
# 即使 LLM 返回了 ```json ... ``` 标记，parser 也能自动提取内容
parser = JsonOutputParser(pydantic_object=MathResult)

try:
    # 尝试解析
    output = parser.parse(content)
    print(f"解析成功 -> 工具入参: {output['args']}, 计算结果: {output['result']}")
except Exception:
    # 如果 parser 失败，尝试作为纯 JSON 解析
    try:
        # 去掉可能的 markdown 标记再转
        clean_content = content.replace("```json", "").replace("```", "").strip()
        output = json.loads(clean_content)
        print(f"JSON解析成功 -> 计算结果: {output['result']}")
    except json.JSONDecodeError:
        print(f"解析失败，原始输出: {content}")
