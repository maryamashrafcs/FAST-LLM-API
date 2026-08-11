from pydantic import BaseModel, Field
from typing import Optional

class LLMRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="The user prompt to send to the LLM")
    system_prompt: Optional[str] = Field(None, description="Optional system instructions")

class LLMResponse(BaseModel):
    content: str
    model: str
    stubbed: bool = False