import subprocess
import sys
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types

# --- ÉP ĐỊNH DẠNG UTF-8 CHO TERMINAL ---
sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')
# ---------------------------------------

# 1. Khởi tạo ứng dụng FastAPI
# --- THÊM 2 DÒNG NÀY ---
from dotenv import load_dotenv
load_dotenv()
# -----------------------
app = FastAPI(title="Robot Teacher Brain API")

# Lấy API Key từ biến môi trường (AWS)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chưa thiết lập biến môi trường GEMINI_API_KEY")

client = genai.Client(api_key=api_key)


# 2. Định nghĩa công cụ MCP (Tool)
def calculate(expression: str) -> str:
    """Thực hiện các phép tính toán học. Truyền vào biểu thức toán học."""
    print(f"[API Server] Đang gọi công cụ tính toán: {expression}")
    try:
        process = subprocess.Popen(
            [sys.executable, 'calculator.py', expression],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout, stderr = process.communicate()
        return stdout.strip() if process.returncode == 0 else f"Lỗi tính toán: {stderr}"
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"


# 3. Khởi tạo phiên trò chuyện (Chat Session)
config = types.GenerateContentConfig(
    tools=[calculate],
    system_instruction=(
        "Bạn là Robot dạy học thông minh. "
        "BẮT BUỘC dùng công cụ 'calculate' nếu có phép toán. "
        "Xưng hô: Robot - Bé. Trả lời ngắn gọn, vui vẻ."
    ),
    temperature=0.5,
)

# Khởi tạo một phiên chat toàn cục (để nhớ ngữ cảnh)
chat_session = client.chats.create(model='gemini-2.5-flash', config=config)


# 4. Định nghĩa cấu trúc dữ liệu giao tiếp (Payload Schema)
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str

# 5. Mở cổng API để phần cứng gọi tới
@app.post("/api/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest): # <--- Đã xóa chữ 'async'
    try:
        # Tự tin mở lại lệnh print
        print(f"Nhận từ phần cứng: {request.message}")

        # Gửi nội dung tới Gemini
        response = chat_session.send_message(request.message)

        # Tự tin mở lại lệnh print
        print(f"Trả về phần cứng: {response.text}")
        return ChatResponse(reply=response.text)

    except Exception as e:
        # In lỗi ra màn hình đen để dễ sửa nếu có vấn đề
        import traceback
        print("\n=== LỖI CHI TIẾT ===")
        traceback.print_exc()
        print("====================\n")
        raise HTTPException(status_code=500, detail=str(e))