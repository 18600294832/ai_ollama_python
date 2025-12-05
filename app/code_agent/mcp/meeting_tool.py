from mcp.server.fastmcp import FastMCP
import subprocess
import shlex
from typing import Annotated
from pydantic import Field
mcp = FastMCP()


@mcp.tool(name="create_meeting", description="创建会议")
def run_shell_command(meeting_name: Annotated[str, Field(description="创建的会议名称", examples="dy的会议")]):
    command = f"mkdir {meeting_name}"
    subprocess.run(command, shell=True, capture_output=True, text=True)


@mcp.tool(name="close_meeting", description="删除会议")
def run_shell_command(meeting_name: Annotated[str, Field(description="创建的会议名称", examples="dy的会议")]):
    command = f"rm -rf {meeting_name}"
    subprocess.run(command, shell=True, capture_output=True, text=True)


if __name__ == "__main__":
    mcp.run(transport="stdio")
