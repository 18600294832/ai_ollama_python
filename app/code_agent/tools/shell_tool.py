from app.code_agent.util.mcp_util import create_mcp_stdio_client
import asyncio

async def get_stdio_shell_tools():
    params = {
        "command": "python",
        "args": [
            "/Users/dingyu/Documents/company/ai_ollama_python/app/code_agent/mcp/shell_tool.py"
        ]
    }

    client, tools = await create_mcp_stdio_client("shell_tools", params)
    return tools


