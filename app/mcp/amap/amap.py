import os
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio
from langchain.agents import create_agent
from app.mcp.common import llm
from langchain.messages import HumanMessage


async def create_amap_mcp_client():
    amap_key = os.getenv("AMAP_KEY")
    mcp_config = {
        "amap": {
            "url": f"https://mcp.amap.com/mcp?key={amap_key}",
            "transport": "streamable_http",
        }
    }
    client = MultiServerMCPClient(mcp_config)

    tools = await client.get_tools()

    return client, tools


async def create_and_run_agent():
    client, tools = await create_amap_mcp_client()
    agent = create_agent(
        llm,
        tools=tools,
        system_prompt="你是一个地图查询专家，擅长回答地图查询问题",
    )
    store = agent.store
    print("----------")
    print(store)
    print("+++++")
    user_task = """
        帮我规划一条过年从北京回山东枣庄的路线
    """
    task = {
        "messages": [HumanMessage(content=user_task)]
    }
    resp = await agent.ainvoke(task)
    print(resp)


asyncio.run(create_and_run_agent())
