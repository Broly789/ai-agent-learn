import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain.agents import create_agent
from app.bailian.common import llm


# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
async def create_stdio_client():
    """
    创建并连接到一个通过 stdio 通信的 MCP 服务器。

    该函数会启动一个子进程运行 mcp_stdin_server.py，
    建立会话，初始化并加载可用的工具列表。
    """
    # 配置服务器参数：使用 python3 执行当前的 server 脚本
    server_params = StdioServerParameters(
        command="npx",
        args=["-y", "@playwright/mcp@latest"],
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

            response = await agent.ainvoke(input = {"messages": [("user", "在bilibili网站搜索周杰伦")]})

            # 提取最终结果
            # final_message = result['messages'][-1]
            # print(f"\n最终结果: {final_message.content}")
            print(response)
            # return result


# 入口点：运行异步主函数
if __name__ == "__main__":
    asyncio.run(create_stdio_client())
