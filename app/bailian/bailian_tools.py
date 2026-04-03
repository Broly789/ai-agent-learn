from app.bailian.common import chat_prompt_template, llm
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class AddInput(BaseModel):
    a: int = Field(description="第一个加数")
    b: int = Field(description="第二个加数")

@tool(args_schema=AddInput)
def add(a: int, b: int) -> int:
    """一个数学专家，能够计算两个数字的和。
    
    计算两个整数的和 (add two numbers)
    """
    return a + b

# 创建工具列表和名称映射
tools = [add]
tools_map = {tool.name: tool for tool in tools}

llm_with_tools = llm.bind_tools(tools)

chain = chat_prompt_template | llm_with_tools

resp = chain.invoke(input={"role": "数学专家", "something": "计算 100+200=?"})

print("=== LLM 响应 ===")
print(f"内容：{resp.content}")
print(f"工具调用：{resp.tool_calls}")

# 处理工具调用
if resp.tool_calls:
    print("\n=== 执行工具调用 ===")
    for tool_call in resp.tool_calls:
        tool_name = tool_call['name']
        args = tool_call['args']
        
        print(f"调用工具：{tool_name}")
        print(f"参数：{args}")
        
        # 根据工具名称自动获取对应的 Tool 对象
        if tool_name in tools_map:
            tool_func = tools_map[tool_name]
            result = tool_func.invoke(args)
            print(f"计算结果：{result}")
        else:
            print(f"警告：未找到工具 '{tool_name}'")

