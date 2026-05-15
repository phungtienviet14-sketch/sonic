import subprocess
import sys
import os
from google import genai
from google.genai import types

# Cấu hình API Key với SDK mới (Thay YOUR_GEMINI_API_KEY bằng key thật)
client = genai.Client(api_key="AIzaSyDQXFXnXeswVQR_2chhN8gY5E2Q1K39jlc")


# ---------------------------------------------------------
# 1. Khai báo "Kỹ năng" (Tool)
# ---------------------------------------------------------
def calculate(expression: str) -> str:
    """Thực hiện các phép tính toán học phức tạp. Truyền vào biểu thức toán học."""
    print(f"\n[Hệ thống MCP] Đang gọi công cụ tính toán: {expression}")

    try:
        # Dùng sys.executable để gọi đúng môi trường ảo .venv của PyCharm
        process = subprocess.Popen(
            [sys.executable, 'calculator.py', expression],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8'
        )
        stdout, stderr = process.communicate()

        if process.returncode == 0:
            return stdout.strip()
        else:
            return f"Lỗi tính toán: {stderr}"
    except Exception as e:
        return f"Lỗi hệ thống: {str(e)}"


# ---------------------------------------------------------
# 2. Cấu hình Model & Chat Session
# ---------------------------------------------------------
# Khởi tạo cấu hình cho model, đưa tool tính toán vào
config = types.GenerateContentConfig(
    tools=[calculate],
    system_instruction=(
        "Bạn là Robot dạy học thông minh cho trẻ em. "
        "Khi có các phép tính, bạn PHẢI sử dụng công cụ 'calculate'. "
        "Sau khi có kết quả, hãy giải thích nhẹ nhàng, vui vẻ cho bé. "
        "Xưng hô: Robot - Bé."
    ),
    temperature=0.5,
)

# Chuyển sang model gemini-2.5-flash mới nhất để Function Calling hoạt động ổn định nhất
chat = client.chats.create(
    model='gemini-2.5-flash',
    config=config
)


def ask_robot(question: str):
    print(f"👤 Bé: {question}")
    response = chat.send_message(question)
    print(f"🤖 Robot: {response.text}\n")


# ---------------------------------------------------------
# 3. Chạy chương trình
# ---------------------------------------------------------
if __name__ == "__main__":
    print("--- Robot Dạy Học Sẵn Sàng (SDK google-genai) ---\n")

    # Tự động tạo file calculator.py (nhân viên kế toán) nếu chưa có trong thư mục sonic
    calc_path = "calculator.py"
    if not os.path.exists(calc_path):
        with open(calc_path, "w", encoding="utf-8") as f:
            f.write("import sys\ntry:\n    print(eval(sys.argv[1]))\nexcept Exception as e:\n    print('Lỗi:', e)\n")

    # Chạy thử 2 kịch bản
    ask_robot("Robot ơi, 1234 nhân với 56 bằng bao nhiêu?")
    ask_robot("Mẹ cho bé 100 nghìn, bé mua 3 cái kem mỗi cái 12 nghìn. Robot tính giúp bé xem còn lại bao nhiêu tiền?")