import os
import asyncio
import logging
from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.callbacks import StdOutCallbackHandler

from app.bailian.common import llm, file_tools
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv

# 配置日志格式和级别
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 加载环境变量，自动读取项目根目录的 .env 文件
load_dotenv("../../../.env")
load_dotenv("../../../.env.local", override=True)

async def create_amap_mcp_client():
    """
    创建并初始化高德地图 MCP 客户端
    
    Returns:
        tuple: (client, tools) - MCP 客户端实例和可用的工具列表
    """
    # 从环境变量中获取高德 MCP API Key
    amap_key = os.getenv("AMAP_MCP_API_KEY")
    
    # 配置 MCP 服务器连接参数
    mcp_config = {
        "amap": {
            "url": f"https://mcp.amap.com/sse?key={amap_key}&format=1",
            "transport": "sse"  # 使用 Server-Sent Events 传输协议
        }
    }
    
    # 创建多服务器 MCP 客户端
    client = MultiServerMCPClient(mcp_config)
    
    # 异步获取所有可用的工具
    tools = await client.get_tools()

    return client, tools

# asyncio.run(create_amap_mcp_client())

async def create_and_run_agent():
    """
    创建并运行智能体，处理用户关于地图路线规划和文件操作的请求
    """
    # 初始化高德 MCP 客户端并获取工具
    client, tools = await create_amap_mcp_client()

    # 创建智能体，绑定大语言模型和高德地图工具及文件操作工具
    agent = create_agent(model=llm, tools=tools + file_tools)
    
    # 定义提示词模板，设定智能体的角色和能力
    prompt_template = PromptTemplate.from_template(
        template="你是一个文件管理助手 + 高德助手,你可以根据用户的问题,使用高德地图MCP 工具 来获取地图信息。也可以使用文件管理工具来操作文件。用户的问题是:{input}"
    )
    
    # 格式化提示词，包含具体的用户任务需求
    prompt = prompt_template.format(input="""
   问题：明天早上8点北京燕丹村到北京什刹海的公交地铁路线规划?
   要求制作成html5页面展示出来路线,
   网页简约美观风格，以及卡片展示 天气状况 穿衣建议
   路线规划点击可以唤起高德app 展示路线
   将生成的html页面输出到 ./amap_route.html
    """)
   
    # 记录开始执行日志
    logger.info(f"开始执行 Agent,用户问题: {prompt}")
    logger.info("="*50)
   
    # 调用智能体执行任务，并使用回调处理器显示工具调用过程
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": prompt}]},
        config={"callbacks": [StdOutCallbackHandler()]}
    )
   
    # 记录执行完成日志和最终结果
    logger.info("Agent 执行完成")
    logger.info(f"最终结果: {result}")
    
    return result

# 入口点：运行异步主函数
asyncio.run(create_and_run_agent())