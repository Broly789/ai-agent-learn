from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import create_agent
from app.bailian.common import llm

# 1. 定义工具
tools = [PythonREPLTool()]

# 2. 定义系统规范 (System Prompt) - 专门约束智能体的行为和输出质量
# 将你所有的排版要求、响应式要求和路径要求放进这里
system_prompt = """你是一个全栈开发专家。
你的任务是编写响应式的电商企业官网代码，必须严格遵循以下开发规范：
1. 使用 HTML5/CSS3，必须实现移动端与 PC 端的响应式适配（媒体查询）。
2. 代码排版必须结构清晰、格式规范，严禁所有元素堆叠在一行。
3. 必须通过调用 PythonREPLTool，将生成的完整 HTML 代码保存到指定文件：
   /Users/brolylee/2026web/ai-agent/.temp/index3.html
4. 确保生成的 HTML 代码是完整可运行的。
"""

# 3. 初始化 Agent
agent = create_agent(llm, tools, system_prompt=system_prompt)

# 4. 定义业务需求 (User Input)
# 此处仅描述“要做什么”，不包含行为规范
user_task = """创建一个电商企业官网，包含商品列表、banner。"""

# 5. 执行调用
result = agent.invoke({
    "messages": [
        {"role": "user", "content": user_task}
    ]
})

# 打印结果
print(result["messages"][-1].content)
