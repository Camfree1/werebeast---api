from fastapi import FastAPIfrom pydantic import BaseModelimport requestsimport time
app = FastAPI()
KLING_API_KEY = "your_kling_api_key_here"
class GenerateRequest(BaseModel):    prompt: str    image_url: str # user's uploaded photo URL from Bubble
@app.post("/generate")def generate(data: GenerateRequest):        # Step 1 - Send job to Kling    response = requests.post(        "https://api.klingai.com/v1/videos/image2video",        headers={            "Authorization": f"Bearer {KLING_API_KEY}",            "Content-Type": "application/json"        },        json={            "model_name": "kling-v1-6",            "image": data.image_url,            "prompt": data.prompt,            "duration": "5",            "mode": "pro"        }    )
    job = response.json()    task_id = job["data"]["task_id"]
    # Step 2 - Poll until video is ready    for i in range(30):        time.sleep(5)        poll = requests.get(            f"https://api.klingai.com/v1/videos/image2video/{task_id}",            headers={"Authorization": f"Bearer {KLING_API_KEY}"}        )        result = poll.json()        status = result["data"]["task_status"]
        if status == "succeed":            video_url = result["data"]["works"][0]["resource"]["resource"]            return {"status": "success", "video_url": video_url}        elif status == "failed":            return {"status": "failed", "error": "Kling job failed"}
    return {"status": "timeout", "error": "Video took too long"}
