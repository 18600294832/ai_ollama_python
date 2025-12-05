import os
from langchain_mcp_adapters.client import MultiServerMCPClient


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
    return tools
