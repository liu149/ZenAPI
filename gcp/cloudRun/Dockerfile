FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src /app/src

# 使用 shell 形式的 CMD 来允许环境变量替换
CMD uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}
