import json
import subprocess

# ---------------------------------------------------------
# 1. Định nghĩa "Nhân cách" và Kịch bản cho Robot (System Prompt)
# ---------------------------------------------------------
ROBOT_SYSTEM_PROMPT = """
Bạn là một Robot dạy học thông minh, thân thiện và kiên nhẫn dành cho trẻ em (từ 6-10 tuổi).
Nhiệm vụ của bạn là hỗ trợ các bé làm bài tập toán, trả lời câu hỏi khoa học và tổ chức trò chơi.
QUY TẮC QUAN TRỌNG:
- Không bao giờ tự nhẩm tính các phép toán phức tạp (nhân, chia số lớn, đổi đơn vị).
- BẮT BUỘC phải sử dụng công cụ 'calculator' để tính toán trước khi đưa ra câu trả lời cuối cùng cho bé.
- Giọng điệu luôn vui vẻ, xưng "Robot" và gọi người dùng là "Bé" hoặc "Em".
- Nếu bé làm sai, hãy hướng dẫn từng bước chứ không chỉ đưa ra đáp án.
"""


# ---------------------------------------------------------
# 2. Giả lập hàm gọi LLM có tích hợp Tool (Conceptual)
# ---------------------------------------------------------
def call_llm_with_tools(user_input):
    """
    Hàm này mô phỏng việc gửi Prompt đến LLM (như Gemini/OpenAI API).
    LLM sẽ quyết định xem có cần gọi Tool không dựa trên user_input.
    """
    print(f"[Robot Đang Suy Nghĩ...] Phân tích câu nói: '{user_input}'")

    # Logic giả lập: Nếu câu hỏi có chứa số và phép toán, LLM quyết định gọi MCP
    if "nhân" in user_input or "*" in user_input:
        print("[LLM Quyết Định] Cần tính toán chính xác, chuẩn bị gọi mcp-calculator...")

        # Bóc tách phép tính (Trong thực tế, LLM tự làm việc này và sinh ra JSON request)
        expression = "15 * 48"  # Lấy ví dụ từ Kịch bản 1

        # Gọi công cụ ngoại vi (giao tiếp với tiến trình mcp-calculator)
        result = execute_mcp_calculator(expression)

        # LLM nhận kết quả và tổng hợp thành câu nói tự nhiên
        final_response = f"Robot đã tính xong rồi! Kết quả của phép tính {expression} chính xác là {result}. Bé làm gần đúng rồi, mình cùng kiểm tra lại nhé!"
        return final_response
    else:
        return "Bé ơi, Robot nghe chưa rõ phép tính, bé đọc lại cho Robot được không?"


# ---------------------------------------------------------
# 3. Giao tiếp với MCP Server qua Subprocess (stdio)
# ---------------------------------------------------------
def execute_mcp_calculator(expression):
    """
    Khởi chạy và giao tiếp với dự án mcp-calculator.
    Đây chính là luồng giao thức (Pipe) đẩy lệnh xuống 'Phòng Kế toán'.
    """
    print(f"[MCP Client] Gửi yêu cầu tính toán: {expression}")

    # Payload chuẩn JSON-RPC của MCP
    mcp_request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "execute_tool",
        "params": {
            "name": "calculate",
            "arguments": {"expression": expression}
        }
    }

    try:
        # Trong môi trường thực tế, mcp-calculator có thể chạy như một process daemon.
        # Ở đây ta giả lập gọi lệnh CLI cơ bản.
        # Lưu ý: Thay 'python mcp-calculator/calculator.py' bằng đúng entrypoint của repo.
        process = subprocess.Popen(
            ['python', 'mcp-calculator/calculator.py', expression],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            print(f"[MCP Server] Trả kết quả: {stdout.strip()}")
            return stdout.strip()
        else:
            return f"Lỗi tính toán: {stderr}"
    except Exception as e:
        return str(e)


# ---------------------------------------------------------
# 4. Vòng lặp giao tiếp chính (Console Interface)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=======================================")
    print("🤖 ROBOT DẠY HỌC ĐÃ KHỞI ĐỘNG 🤖")
    print("=======================================")

    # Test Kịch bản 1: Trợ lý kiểm tra bài tập
    user_message = "Robot ơi, bài này con tính: 15 thùng sữa nhân 48 hộp là 700 hộp, đúng không?"
    print(f"\n👤 Bé nói: {user_message}\n")

    response = call_llm_with_tools(user_message)
    print(f"🤖 Robot trả lời: {response}\n")