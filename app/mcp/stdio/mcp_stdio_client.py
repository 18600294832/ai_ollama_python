from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
from langchain.agents import create_agent
from app.mcp.common import llm
from langchain.messages import HumanMessage

async def create_mcp_stdio_client():
    server_params = StdioServerParameters(
        command="python3",
        args=["/Users/dingyu/Documents/company/ai_ollama_python/app/mcp/stdio/mcp_stdio_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await load_mcp_tools(session)
            print(tools)

            agent = create_agent(
                llm,
                tools=tools,
                system_prompt="你是一个计算专家",
            )
            resp = await agent.ainvoke({"messages": [HumanMessage(content="1 + 2 * 5 = ?")]})
            print(resp)


asyncio.run(create_mcp_stdio_client())
