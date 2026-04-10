import os
import asyncio
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession, Tool
from mcp.client.stdio import stdio_client
from langchain.agents import create_agent
from app.bailian.common import llm

# 正确加载优先级的环境变量文件
load_dotenv("../../../.env")
load_dotenv("../../../.env.local", override=True)

# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
async def create_stdio_client():
    """
    创建并连接到一个通过 stdio 通信的 MCP 服务器。

    该函数会启动一个子进程运行 mcp_stdin_server.py，
    建立会话，初始化并加载可用的工具列表。
    """
    # 配置服务器参数：使用 python3 执行当前的 server 脚本
    github_access_token = os.getenv("GITHUB_PERSONAL_ACCESS_TOKEN")
    server_params = StdioServerParameters(
        args=[
        "-y",
        "@modelcontextprotocol/server-github"
         ],
        command="npx",
        env={
                "GITHUB_PERSONAL_ACCESS_TOKEN": f"{github_access_token}"
            }
    )

    # 建立 stdio 客户端连接
    async with stdio_client(server_params) as (read, write):
        # 创建 MCP 客户端会话
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()

            # 从会话中加载 MCP 工具
            tools = await load_mcp_tools(session)
            # 打印加载到的工具信息
            print(f"成功加载 {len(tools)} 个工具:")
            for tool in tools:
                print(f" - {tool.name}: {tool.description}")
            agent = create_agent(llm, tools, debug=True)

            response = await agent.ainvoke(input = {"messages": [("user", "在github上搜索vue-element-admin项目 ，并给我项目介绍")]})

            # 提取最终结果
            messages = response["messages"]
            for message in messages:
                if isinstance(message, HumanMessage):
                    print("用户:", message.content)
                elif isinstance(message, AIMessage):
                    if message.content:
                        print("助手:", message.content)
                    else:
                       for tool_call in message.tool_calls:
                           print("助手[调用工具]:", tool_call["name"], tool_call["args"])
                elif isinstance(message, ToolMessage):
                    print("助手[工具调用]:", message.name)
            # return result


# 入口点：运行异步主函数
if __name__ == "__main__":
    asyncio.run(create_stdio_client())
