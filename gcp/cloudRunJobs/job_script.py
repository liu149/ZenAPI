import time
from datetime import datetime

def main():
    print(f"Job started at {datetime.now()}")
    # 这里放置您的任务逻辑
    time.sleep(10)  # 模拟一些处理时间
    print(f"Job completed at {datetime.now()}")

if __name__ == "__main__":
    main()
