from typing import Any
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda, RunnableParallel, RunnablePassthrough, RunnableBranch
from app.bailian.common import llm

lambda_chain = RunnableLambda(lambda x: x.upper())
lambda_chain2 = RunnableLambda(lambda x: x + "!")

# chain = lambda_chain | lambda_chain2
branch1_lambda = RunnableLambda(lambda x: x.upper())
branch2_lambda = RunnableLambda(lambda x: x + "!")
default_branch = RunnableLambda(lambda x: x)

chain = llm | StrOutputParser() | RunnableBranch(
    (lambda x: "question" in x, branch1_lambda),  # type: ignore
    (lambda x: "answer" in x, branch2_lambda),  # type: ignore
    default_branch  # type: ignore
)

print(chain.invoke("原样返回question"))
print(chain.invoke("原样返回answer"))


