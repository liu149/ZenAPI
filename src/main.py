from fastapi import FastAPI
import time
import math

app = FastAPI()

def cpu_intensive_task(n: int):
    start = time.time()
    while time.time() - start < n:
        [math.sqrt(i) for i in range(10000)]

# kubernetes backend service will call this endpoint to check if the service is running
@app.get("/")
async def root():
    return {"status": "OK"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.get("/cpu-task/{seconds}")
async def cpu_task(seconds: int):
    cpu_intensive_task(seconds)
    return {"message": f"CPU intensive task completed for {seconds} seconds"}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}