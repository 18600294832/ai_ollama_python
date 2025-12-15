from langchain_openai import ChatOpenAI
import os

llm_qwen = ChatOpenAI(
    model="qwen3-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    streaming=True,
)
