from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
import asyncio
from langchain.agents import create_agent
from app.mcp.common import llm
from langchain.messages import HumanMessage


# 获取mcp的tools
async def mcp_play_wright_client():
    server_params = StdioServerParameters(
        command="node",
        args=["/Users/dingyu/.nvm/versions/node/v18.15.0/lib/node_modules/@executeautomation/playwright-mcp-server/dist/index.js"]
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            # 获取mcp tools
            tools = await load_mcp_tools(session)

            print(tools)
            print("--- ----")
            agent = create_agent(llm, tools)
            #

            resp = await agent.ainvoke({
                "messages": [
                    [HumanMessage(content="在百度中查询北京今天的天气怎么样")]
                ]
            })

asyncio.run(mcp_play_wright_client())
