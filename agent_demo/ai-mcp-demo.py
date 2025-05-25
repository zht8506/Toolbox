# from https://gist.github.com/cradiator/76629158bec2140368fa8ac1796f4814
# 【8分钟教会你写 MCP】 https://www.bilibili.com/video/BV1nyVDzaE1x/?share_source=copy_web&vd_source=de9e397f0646c3eab70729a000c35008

# main.py
from mcp.server.fastmcp import FastMCP
import tools

mcp = FastMCP("host info mcp")
mcp.add_tool(tools.get_host_info)

@mcp.tool()
def foo():
    return ""

def main():
    mcp.run("stdio") # sse


if __name__ == "__main__":
    main()

    
# tools.py
import platform
import psutil
import subprocess
import json

def get_host_info() -> str:
    """get host information

    Returns:
        str: the host information in JSON string
    """
    info: dict[str, str] = {
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "memory_gb": str(round(psutil.virtual_memory().total / (1024**3), 2)),
    }

    cpu_count = psutil.cpu_count(logical=True)
    if cpu_count is None:
        info["cpu_count"] = "-1"
    else:
        info["cpu_count"] = str(cpu_count)
    
    try:
        cpu_model = subprocess.check_output(
            ["sysctl", "-n", "machdep.cpu.brand_string"]
        ).decode().strip()
        info["cpu_model"] = cpu_model
    except Exception:
        info["cpu_model"] = "Unknown"

    return json.dumps(info, indent=4)

if __name__ == '__main__':
    print(get_host_info())
