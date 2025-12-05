from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.redis import RedisSaver
from langchain.agents import create_agent
from app.code_agent.model.qwen import llm_qwen
from app.code_agent.tools.file_tools import file_tools
from langchain_core.runnables import RunnableConfig
import asyncio

from app.code_agent.tools.shell_tool import get_stdio_shell_tools
from app.code_agent.tools.amap_tools import create_amap_mcp_client
from app.code_agent.tools.meeting_tool import get_meeting_tool
from app.code_agent.tools.


async def run_agent():
    shell_tools = await get_stdio_shell_tools()
    amap_tools = await create_amap_mcp_client()
    meeting_tools = await get_meeting_tool()
    terminal_tools = await get_stdio_terminal_tools()
    tools = shell_tools + file_tools + amap_tools + meeting_tools
    agent = create_agent(
        model=llm_qwen,
        tools=tools,
        checkpointer=InMemorySaver(),
        debug=True,
    )

    config = RunnableConfig(configurable={"thread_id": 9})

    while True:
        user_input = input("用户：")
        if user_input.lower() == "exit" or user_input.lower() == "quit" or user_input.lower() == "q":
            break

        resp = agent.astream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode="messages",
        )
        # print("=-===")
        # print(resp)
        # print("----")
        async for token, metadata in resp:
            print(token.content, end="", flush=True)

        print("\n")

    print("\n============\n")


def print_content_blocks(token):
    """只输出纯文本内容"""
    print("------------")
    print(token.content, end="", flush=True)
    print("-------token-----")
    if token.content_blocks:
        for block in token.content_blocks:
            if isinstance(block, dict) and 'text' in block:
                print("block:\n")
                print(block['text'], end="", flush=True)



asyncio.run(run_agent())
