# 导入 FastMCP：快速开发 MCP 服务端的官方框架
from mcp.server.fastmcp import FastMCP

# 创建一个 MCP 服务，名字叫 stdio_mcp（标识用）
mcp = FastMCP("stdio_mcp", stateless_http= True, json_response=True)

# --------------------
# 工具 1：加法函数
# --------------------
@mcp.tool()  # ✅ 装饰器：把这个函数注册成 AI 可调用的工具
def add(a: int, b: int) -> int:
    """一个数学专家，能够计算两个数字的和。
    计算两个整数的和 (add two numbers)
    """
    return a + b  # 真正执行逻辑：返回两数之和

# --------------------
# 工具 2：乘法函数
# --------------------
@mcp.tool()  # ✅ 同样注册成工具
def mul(a: int, b: int) -> int:
    """一个数学专家，能够计算两个数字的乘积。
    计算两个整数的乘积 (multiply two numbers)
    """
    return a * b  # 真正执行逻辑：返回乘积

# --------------------
# 启动服务
# --------------------
if __name__ == "__main__":
    mcp.run(transport="streamable-http")