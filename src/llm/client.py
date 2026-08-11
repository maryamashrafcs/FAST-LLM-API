import os
from groq import Groq
from dotenv import load_dotenv
from src.llm.schemas import LLMRequest, LLMResponse

load_dotenv()

def generate_llm_response(request: LLMRequest) -> LLMResponse:
    is_stub = os.getenv("LLM_STUB", "0") == "1"
    model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

    # Offline Stub Mode
    if is_stub:
        return LLMResponse(
            content=f"[STUB RESPONSE] Mock output for prompt: '{request.prompt}'",
            model=model_name,
            stubbed=True
        )

    # Live Groq API Call
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set in environment variables.")

    client = Groq(api_key=api_key)
    
    messages = []
    if request.system_prompt:
        messages.append({"role": "system", "content": request.system_prompt})
    messages.append({"role": "user", "content": request.prompt})

    response = client.chat.completions.create(
        model=model_name,
        messages=messages
    )

    return LLMResponse(
        content=response.choices[0].message.content,
        model=model_name,
        stubbed=False
    )