from langchain_classic.output_parsers import BooleanOutputParser, DatetimeOutputParser
from langchain_core.output_parsers import CommaSeparatedListOutputParser, JsonOutputParser
from app.bailian.common import chat_prompt_template, llm
from pydantic import BaseModel, Field

# 1. 定义你想要的结构 (Pydantic 模型)
class UserInfo(BaseModel):
    name: str = Field(description="姓名")
    age: int = Field(description="年龄")

# output_parser = StrOutputParser()
# output_parser = CommaSeparatedListOutputParser()
# output_parser = BooleanOutputParser()
output_parser = JsonOutputParser(pydantic_object=UserInfo)

format_instructions = output_parser.get_format_instructions()
chain = chat_prompt_template | llm | output_parser

# resp = chain.invoke({"role": "数学", "something": "100+100=200 对吗？请回答 YES 或 NO"})

resp = chain.invoke(input={"role": "娱乐", "something": f"周杰伦对象的姓名和年龄是多少？请严格输出 JSON 结构，格式为：\n{format_instructions}"})
print(resp)
