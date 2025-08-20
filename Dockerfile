# 使用 Python 基底映像檔
FROM python:3.11

# 設定工作目錄
WORKDIR /usr/src/app

# 複製需求檔
COPY requirements.txt .

# 安裝需求套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 啟動 FastAPI (uvicorn)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]