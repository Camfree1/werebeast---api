rom pydantic import BaseModel
class GenerateRequest(BaseModel):    prompt: str
@app.post("/generate")def generate(data: GenerateRequest):    return {        "status": "success",        "prompt_received": data.prompt    }
