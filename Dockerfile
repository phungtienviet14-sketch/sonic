FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy mã nguồn API và Tool vào container
COPY api_server.py calculator.py ./

# Mở cổng 8000 cho container
EXPOSE 8000

# Khởi chạy API server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]