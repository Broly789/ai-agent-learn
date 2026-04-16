from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel

from app.bailian.common import llm

joke_chain = ChatPromptTemplate.from_template(
    "请讲一个笑话主题：{topic}"
) | llm
poem_chain = ChatPromptTemplate.from_template(
    "请写一个唐诗主题：{topic}"
) | llm

parallel_chain = RunnableParallel(
    joke = joke_chain,
    poem = poem_chain
)

result = parallel_chain.invoke({"topic": "周杰伦"})
print(result)
