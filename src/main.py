from fastapi import FastAPI
import time
import math

app = FastAPI()

def cpu_intensive_task(n: int):
    start = time.time()
    while time.time() - start < n:
        [math.sqrt(i) for i in range(10000)]

@app.get("/cpu-task/{seconds}")
async def cpu_task(seconds: int):
    cpu_intensive_task(seconds)
    return {"message": f"CPU intensive task completed for {seconds} seconds"}

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}