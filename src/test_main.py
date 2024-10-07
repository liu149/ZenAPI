import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from fastapi.testclient import TestClient
from main import app  # 直接导入 main，不使用 src

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_read_item():
    response = client.get("/items/foo", params={"q": "bar"})
    assert response.status_code == 200
    assert response.json() == {"item_id": "foo", "q": "bar"}

def test_cpu_task():
    response = client.get("/cpu-task/1")
    assert response.status_code == 200
    assert "CPU intensive task completed for 1 seconds" in response.json()["message"]