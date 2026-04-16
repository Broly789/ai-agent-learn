import os
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, ChatMessagePromptTemplate, FewShotPromptTemplate
from langchain_core.tools import tool
from langchain_community.agent_toolkits import FileManagementToolkit
from pydantic import BaseModel, Field
load_dotenv("/Users/brolylee/2026web/ai-agent/.env")
load_dotenv("/Users/brolylee/2026web/ai-agent/.env.local", override=True)
api_key = os.getenv("BAILIAN_QWEN_API_KEY")
if not api_key:
    raise ValueError("BAILIAN_QWEN_API_KEY environment variable is not set")

llm = ChatOpenAI(
     model="qwen3.5-plus",
     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
     api_key=SecretStr(api_key),
     streaming= True
)

system_prompt = ChatMessagePromptTemplate.from_template(
    template="你是一个{role}专家",
    role="system"
)
user_prompt = ChatMessagePromptTemplate.from_template(
    template="{something}",
    role="user"
)

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_prompt,
    user_prompt
])

class AddInput(BaseModel):
    a: int = Field(description="第一个加数")
    b: int = Field(description="第二个加数")

@tool(args_schema=AddInput)
def add(a: int, b: int) -> int:
    """一个数学专家，能够计算两个数字的和。

    计算两个整数的和 (add two numbers)
    """
    return a + b

def create_calc_tools():
    return [add]

calc_tools = create_calc_tools()

structured_llm = llm.with_structured_output(AddInput)

file_toolkit = FileManagementToolkit(root_dir="/Users/brolylee/2026web/ai-agent/.temp")
file_tools = file_toolkit.get_tools()