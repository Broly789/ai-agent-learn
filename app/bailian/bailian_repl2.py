from langchain_core.prompts import PromptTemplate
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import create_agent

from app.bailian.common import llm

tools = [PythonREPLTool()]
tool_names = ["PythonREPLTool"]

agent = create_agent(llm, tools)

# 创建提示词模板
prompt_template = PromptTemplate.from_template(
    """你是一个全栈开发专家。你的任务是根据用户需求编写 HTML/JS 代码。
用户输入：{input}"""
)

prompt = prompt_template.format(input="""
创建一个PC电商企业官网 并支持响应式移动端布局，包含商品列表 banner。页面布局一定要符合PC端和移动端的布局规范。之前生成的网页都排在了一行很乱 请认真点。
输出为/Users/brolylee/2026web/ai-agent/.temp/index2.html
""")



result = agent.invoke({"messages": [{"role": "user", "content": prompt}]})
print(result["messages"][-1].content)

