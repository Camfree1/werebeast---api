from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "server is working"}
from pydantic import BaseModel
class VideoRequest(BaseModel):    prompt: str
@app.post("/generate-video")def generate_video(request: VideoRequest):    print("Received prompt:", request.prompt)
    return {        "success": True,        "message": "Route is working",        "promptReceived": request.prompt    }
