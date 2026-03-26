from fastapi import FastAPI
from pydantic import BaseModel
import requests
import time

app = FastAPI()

VEO3_API_KEY =sk-f4ae0351d86f4becbfd003f018a10e73

class GenerateRequest(BaseModel):
    prompt: str
    image_url: str

@app.post("/generate")
def generate(data: GenerateRequest):
    response = requests.post(
        "https://veo3api.com/generate",
        headers={
            Authorization": f"Bearer {VEO3_API_KEY}"
            "Content-Type": "application/json"
        },
        json={
            "prompt": data.prompt,
            "image_url": data.image_url
        }
    )
    job = response.json()
    task_id = job.get("task_id")
    if not task_id:
            return {"status": "error", "error": str(job)}
    for i in range(30):
        time.sleep(5)
        poll = requests.get(
            f"https://veo3api.com/feed?task_id={task_id}",
            headers={"Authorization": f"Bearer {VEO3_API_KEY}"}
        )
        result = poll.json()
        if result.get("status") == "completed":
            return {"status": "success", "video_url": result.get("video_url")}
        elif result.get("status") == "failed":
            return {"status": "failed"}
    return {"status": "timeout"}
