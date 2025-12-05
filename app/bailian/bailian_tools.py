from pydantic import Field,BaseModel

from app.bailian.common import llm, chat_prompt_template
from langchain_core.tools import tool


class AddInputArgs(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool(
    description="add two number",
    args_schema=AddInputArgs,
)
def add(a, b):
    return a + b


# add_tools = Tool.from_function(
#     name="add",
#     func=add,
#     description="加法计算器，输入两个数字，返回它们的和。参数：a (数字), b (数字)",
# )

tool_dict = {
    "add": add,
}

llm_with_tool = llm.bind_tools([add])

chain = chat_prompt_template | llm_with_tool

resp = chain.invoke(
    input={
        "role": "计算",
        "domain": "数学",
        "question": "100+200",
    }
)
print(resp)

for tool_call in resp.tool_calls:
    print(tool_call["name"]),
    args = tool_call["args"]
    print(args)
    funcName = tool_call["name"]
    print(funcName)

    tool_func = tool_dict[funcName]
    result = tool_func.invoke(args)
    print(result)
