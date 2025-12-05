from mcp.server.fastmcp import FastMCP
import subprocess
import time
import shlex
from typing import Annotated
from pydantic import Field

mcp = FastMCP()


@mcp.tool(name="run_applescript", description="运行applescript")
def run_applescript(script: Annotated[str, Field(description="要运行的AppleScript脚本")]) -> dict:
    """运行 AppleScript 脚本"""
    try:
        p = subprocess.Popen(['osascript', '-e', script],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
        output, error = p.communicate()
        return {
            "output": output.decode('utf-8').strip(),
            "error": error.decode('utf-8').strip()
        }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool(name="close_terminal_if_open", description="关闭已打开的终端应用")
def close_terminal_if_open() -> bool:
    """关闭已打开的终端应用"""
    try:
        output, error = run_applescript("""
tell application "System Events"
    if exists process "Terminal" then
        tell application "Terminal" to quit
    end if    
end tell
        """)
        print(output)
        if error:
            return False
        else:
            return True
    except Exception as e:
        print(f"Error closing terminal: {e}")
        return False


@mcp.tool(name="open_new_terminal", description="打开一个新的终端窗口")
def open_new_terminal(window_id: Annotated[str, Field(description="窗口ID，可选")] = "") -> str:
    """打开一个新的终端窗口"""
    try:
        if window_id:
            output, error = run_applescript(f"""
    tell application "Terminal"
        if (count of windows) > 0 then
            set theWindow to window id {window_id}
            set frontmost of theWindow to true
            activate
        else     
            do script ""
            activate
        end if    
    end tell
            """)
        else:
            output, error = run_applescript("""
    tell application "Terminal"
            activate
        if (count of windows) = 0 then 
            delay 0.5
            do script ""
        end if     
    end tell
            """)
        if error:
            print(error)
            return ""
        else:
            time.sleep(1)  # 减少等待时间
            return get_all_terminal_window_ids()
    except Exception as e:
        print(f"Error opening terminal: {e}")
        return ""


@mcp.tool(name="run_script_in_terminal", description="在终端中运行脚本")
def run_script_in_terminal(script: Annotated[str, Field(description="要在终端中运行的脚本")], 
                          window_id: Annotated[str, Field(description="窗口ID，可选")] = "") -> bool:
    """在终端中运行脚本"""
    try:
        # 转义引号以防止AppleScript错误
        escaped_script = script.replace('"', '')
        output, error = run_applescript(f"""
    tell application "Terminal"
        activate
        if (count of windows) > 0 then
            do script "{escaped_script}" in window 1 
        else     
            do script "{escaped_script}"
        end if 
    end tell
        """)
        if error:
            print(error)
            return False
        else:
            return True
    except Exception as e:
        print(f"Error running script in terminal: {e}")
        return False


@mcp.tool(name="get_terminal_full_text", description="获取终端完整文本内容")
def get_terminal_full_text() -> str:
    """获取终端完整文本内容"""
    try:
        output, error = run_applescript("""
tell application "Terminal"
    set fullText to history of selected tab of front window
end tell
        """)
        if error:
            return error
        return output
    except Exception as e:
        return str(e)


@mcp.tool(name="get_all_terminal_window_ids", description="获取所有终端窗口ID")
def get_all_terminal_window_ids() -> str:
    """获取所有终端窗口ID"""
    try:
        output, error = run_applescript("""
tell application "Terminal"
    set outputList to {}
    repeat with aWindow in windows
        set windowID to id of aWindow
        set tabCount to number of tabs of aWindow
        repeat with tabIndex from 1 to tabCount
            set end of outputList to {tab tabIndex of window id windowID}
        end repeat    
    end repeat
end tell
return outputList
        """)
        return output if not error else ""
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    mcp.run(transport="stdio")