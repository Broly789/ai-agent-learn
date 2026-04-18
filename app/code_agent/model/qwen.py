import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr
import os

# 获取项目根目录(app的父目录)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
load_dotenv("/Users/brolylee/2026web/ai-agent/.env")
load_dotenv("/Users/brolylee/2026web/ai-agent/.env.local", override=True)


api_key = os.getenv("BAILIAN_QWEN_API_KEY")
if not api_key:
    raise ValueError("BAILIAN_QWEN_API_KEY environment variable is not set")

llm_qwen = ChatOpenAI(
    model="qwen3.5-plus",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=SecretStr(api_key),
    streaming=True
)