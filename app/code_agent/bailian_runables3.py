from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough
from app.bailian.common import llm

lambda_chain = RunnableLambda(lambda x: x.upper())
lambda_chain2 = RunnableLambda(lambda x: x + "!")

# chain = lambda_chain | lambda_chain2 
chain = llm | StrOutputParser() | RunnableParallel(upper= lambda_chain, origin=RunnablePassthrough())

print(chain.invoke("hello"))


