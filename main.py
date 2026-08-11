from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.llm.schemas import LLMRequest, LLMResponse
from src.llm.client import generate_llm_response

app = FastAPI(
    title="FastAPI LLM Service",
    description="API service providing structured access to Groq LLM with stubbing support.",
    version="1.0.0"
)

# Custom handler to return 400 naming the offending field on invalid input
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    offending_field = errors[0]["loc"][-1] if errors else "body"
    msg = errors[0].get("msg", "Invalid input value")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": f"Invalid input for field '{offending_field}': {msg}"}
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI LLM Service is running!"}

@app.post("/api/llm/generate", response_model=LLMResponse)
def generate_llm(request: LLMRequest):
    try:
        response = generate_llm_response(request)
        return response
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))