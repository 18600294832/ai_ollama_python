from langchain_mcp_adapters.client import MultiServerMCPClient


async def get_meeting_tool():
    params = {
        "command": "python",
        "args": [
            "/Users/dingyu/Documents/company/ai_ollama_python/app/code_agent/mcp/meeting_tool.py"
        ]
    }
    config = {
        "meeting": {
            "transport": "stdio",
            **params
        }
    }
    client = MultiServerMCPClient(config)
    tools = await client.get_tools()
    return tools


