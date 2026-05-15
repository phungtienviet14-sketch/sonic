# # server.py
# from fastmcp import FastMCP
# import sys
# import logging
#
# logger = logging.getLogger('Calculator')
#
# # Fix UTF-8 encoding for Windows console
# if sys.platform == 'win32':
#     sys.stderr.reconfigure(encoding='utf-8')
#     sys.stdout.reconfigure(encoding='utf-8')
#
# import math
# import random
#
# # Create an MCP server
# mcp = FastMCP("Calculator")
#
# # Add an addition tool
# @mcp.tool()
# def calculator(python_expression: str) -> dict:
#     """For mathamatical calculation, always use this tool to calculate the result of a python expression. You can use 'math' or 'random' directly, without 'import'."""
#     result = eval(python_expression, {"math": math, "random": random})
#     logger.info(f"Calculating formula: {python_expression}, result: {result}")
#     return {"success": True, "result": result}
#
# # Start the server
# if __name__ == "__main__":
#     mcp.run(transport="stdio")

import sys

def calculate_expression(expr):
    try:
        # Lưu ý: Hàm eval() dùng để test cục bộ.
        # Trong thực tế, hệ thống MCP sẽ dùng bộ parser an toàn hơn.
        result = eval(expr)
        return result
    except Exception as e:
        return f"Lỗi tính toán: {str(e)}"

if __name__ == "__main__":
    # Lấy biểu thức toán học từ tham số dòng lệnh do Robot truyền vào
    if len(sys.argv) > 1:
        expression = sys.argv[1]
        # Trả kết quả ra màn hình (Robot sẽ đọc luồng này)
        print(calculate_expression(expression))
    else:
        print("Vui lòng cung cấp phép tính.")
