import os
from pydantic import Field, BaseModel
from langchain_core.prompts import ChatPromptTemplate, ChatMessagePromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.structured_output import ToolStrategy

llm = ChatOpenAI(
    model="qwen3-max",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    streaming=True,
)

system_message_template = ChatMessagePromptTemplate.from_template(
    template="你是一个{role}专家，擅长回答{domain}领域问题",
    role="system",
)

agent = create_agent(
    llm,
    tools=[],
    response_format=ToolStrategy(Output),
    system_prompt=system_message_template.content,
)



user_message_template = ChatMessagePromptTemplate.from_template(
    template="用户问题：{question}",
    role="user",
)

chat_prompt_template = ChatPromptTemplate.from_messages([
    system_message_template,
    user_message_template
])


class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool(
    description="add two number",
    args_schema=AddInputArgs,
    return_direct=False,
)
def add(a, b):
    return a + b


def create_calc_tools():
    return [add]


calc_tools = create_calc_tools()
