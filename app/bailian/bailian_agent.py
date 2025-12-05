
from pydantic import BaseModel, Field
from app.bailian.common import llm, create_calc_tools, system_message_template
from langchain.agents import create_agent
from langchain.messages import HumanMessage
from langchain.agents.structured_output import ToolStrategy


class Output(BaseModel):
    args: str = Field(description="调用工具时的入参，如 'add(100, 200)'")
    result: str = Field(description="工具执行后的返回结果，如 '300'")


system_prompt = system_message_template.format(role="计算", domain="数学")


print(system_prompt)
agent = create_agent(
    llm,
    tools=create_calc_tools(),
    response_format=ToolStrategy(Output),
    system_prompt=system_prompt.content,
)


initial_state = {
    "messages": [
        HumanMessage(content="100+200=?")  # 将问题包装成消息对象
    ]
}


resp = agent.invoke(initial_state)
# 直接访问结构化结果
print(resp)
output: Output = resp["structured_response"]
print(f"输出: {output}")
print(f"入参: {output.args}")
print(f"结果: {output.result}")

