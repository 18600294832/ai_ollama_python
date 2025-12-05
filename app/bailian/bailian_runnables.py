from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
import os

llm = ChatOpenAI(
    model="qwen3-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    streaming=True,
)




joke_chain = ChatPromptTemplate.from_template(template="请写一个笑话") | llm
poem_chain = ChatPromptTemplate.from_template(template="请写一首诗") | llm

parallel_chain = RunnableParallel(
    joke=joke_chain,
    poem=poem_chain
)

result = parallel_chain.invoke({"topic": "AI"})
print(result)
