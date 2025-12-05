from mcp.server.fastmcp import FastMCP
import subprocess
import shlex
from typing import Annotated
from pydantic import Field
mcp = FastMCP()


@mcp.tool(name="run_shell_command", description="运行shell命令")
def run_shell_command(command: Annotated[str, Field(description="要运行的shell命令", examples="ls")]) -> str:
    try:
        shell_command = shlex.split(command)
        print(shell_command)
        if "rm" in shell_command:
            return "rm命令被禁止"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            return result.stderr
        return result.stdout
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    mcp.run(transport="stdio")
