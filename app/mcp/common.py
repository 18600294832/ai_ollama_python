from langchain_openai import ChatOpenAI
import os
qwenModel = "qwen3-max"

dashScopeApiKey = os.getenv("DASHSCOPE_API_KEY")


llm = ChatOpenAI(
    model=qwenModel,
    temperature=0.5,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=dashScopeApiKey,
    streaming=True,
)
