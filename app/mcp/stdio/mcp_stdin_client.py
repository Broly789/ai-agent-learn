import asyncio
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client  # 改1：换导入
from langchain.agents import create_agent
from app.bailian.common import llm

# https://github.com/modelcontextprotocol/python-sdk?tab=readme-ov-file#writing-mcp-clients
async def create_http_client():
    """
    连接到 Streamable HTTP MCP 服务器。
    """
    # 改2：用 streamable_http_client 替换 stdio_client
    async with streamable_http_client("http://127.0.0.1:8000/mcp") as (read, write, _):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)
            print(f"成功加载 {len(tools)} 个工具:")
            for tool in tools:
                print(f" - {tool.name}: {tool.description}")

            agent = create_agent(llm, tools)
            from typing import Any
            input_data: Any = {"messages": [{"role": "user", "content": "请计算 12*100=?"}]}
            result = await agent.ainvoke(input_data)

            final_message = result['messages'][-1]
            print(f"\n最终结果: {final_message.content}")
            return result


if __name__ == "__main__":
    asyncio.run(create_http_client())