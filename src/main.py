from fastapi import FastAPI
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件中的环境变量

app = FastAPI()

# Database configuration
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
DB_NAME = os.getenv("DB_NAME", "your_database")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# 使用环境变量来决定是否使用 Cloud SQL Proxy
USE_CLOUD_SQL_PROXY = os.getenv("USE_CLOUD_SQL_PROXY", "false").lower() == "true"

if USE_CLOUD_SQL_PROXY:
    # Cloud SQL Proxy 配置
    INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@127.0.0.1:5432/{DB_NAME}"
else:
    # 本地数据库配置
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

@app.get("/")
async def root():
    return {"status": "OK"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/db-test")
async def db_test():
    try:
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            return {"status": "Database connection successful", "result": result.scalar()}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}