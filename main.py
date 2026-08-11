from fastapi import FastAPI, HTTPException
from src.llm.schemas import LLMRequest, LLMResponse
from src.llm.client import generate_llm_response

app = FastAPI(
    title="FastAPI LLM Service",
    description="API service providing structured access to Groq LLM with stubbing support.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "FastAPI LLM Service is running!"}

@app.post("/api/llm/generate", response_model=LLMResponse)
def generate_llm(request: LLMRequest):
    try:
        response = generate_llm_response(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))