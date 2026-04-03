from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate


llm = ChatOpenAI(
     model="qwen3.5-plus",
     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
     api_key=SecretStr("sk-e8b093d306e94a45a3b95c3f390104d8"),
     streaming= True
)

prompt = PromptTemplate.from_template("{something}是个不错的歌手")

resp = llm.invoke(prompt.format(something="周杰伦"))

print(resp.content)

