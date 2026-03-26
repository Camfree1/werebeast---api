from fastapi import FastAPIfrom pydantic import BaseModelimport requestsimport time
app = FastAPI()
VEO3_API_KEY = sk-f4ae0351d86f4becbfd003f018a10e73
class GenerateRequest(BaseModel):    prompt: str    image_url: str
@app.post("/generate")def generate(data: GenerateRequest):
    # Step 1 - Send job to Veo3    response = requests.post(        "https://veo3api.com/generate",        headers={            "Authorization": f"Bearer sk-f4ae0351d86f4becbfd003f018a10e73",            "Content-Type": "application/json"        },        json={            "prompt": data.prompt,            "image_url": data.image_url,            "model": "veo3-fast",            "watermark": "none"        }    )
    job = response.json()    task_id = job.get("task_id")
    if not task_id:        return {"status": "error", "error": str(job)}
    # Step 2 - Poll until video is ready    for i in range(30):        time.sleep(5)        poll = requests.get(            f"https://veo3api.com/feed?task_id={task_id}",            headers={"Authorization": f"Bearer {VEO3_API_KEY}"}        )        result = poll.json()        status = result.get("status")
        if status == "completed":            video_url = result.get("video_url")            return {"status": "success", "video_url": video_url}        elif status == "failed":            return {"status": "failed", "error": "Veo3 job failed"}
    return {"status": "timeout", "error": "Video took too long"}
