from langchain_openai import ChatOpenAI
from pydantic import SecretStr
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, ChatMessagePromptTemplate, FewShotPromptTemplate

llm = ChatOpenAI(
     model="qwen3.5-plus",
     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
     api_key=SecretStr("sk-e8b093d306e94a45a3b95c3f390104d8"),
     streaming= True
)

# system_prompt = ChatMessagePromptTemplate.from_template(
#     template="你是一个{role}专家",
#     role="system"
# )
# user_prompt = ChatMessagePromptTemplate.from_template(
#     template="{something}",
#     role="user"
# )
#
# prompt = ChatPromptTemplate.from_messages([
#     system_prompt,
#     user_prompt
# ])

# resp = llm.stream(prompt.format_messages(role="web开发专家", something="前端学ai agent开发需要学什么技术栈简单说下"))

few_short_prompt_template = FewShotPromptTemplate(
    examples=[
        {
            "input": "Hello",
            "output": "你好"
        }
    ],
    example_prompt=PromptTemplate.from_template("输入：{input}\n输出：{output}"),
    input_variables=["text"],
    prefix="请将输入翻译成中文",
    suffix="输入：{text}\n输出："
)

prompt = few_short_prompt_template.format(text="respect")
chain = few_short_prompt_template | llm
resp = chain.stream({"text": "respect"})

print(prompt)
# resp = llm.stream(prompt)
for chunk in resp:
    print(chunk.content, end="")
