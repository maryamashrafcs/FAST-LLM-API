from enum import Enum
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CategoryEnum(str, Enum):
    DEVELOPMENT = "Development"
    BUG = "Bug"
    DOCUMENTATION = "Documentation"
    MAINTENANCE = "Maintenance"
    OTHER = "Other"

class PriorityEnum(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    URGENT = "Urgent"

class LLMRequest(BaseModel):
    prompt: str = Field(..., description="The task description to categorize")

    @field_validator("prompt")
    def validate_prompt_not_empty(cls, value: str):
        if not value or not value.strip():
            raise ValueError("prompt cannot be empty or whitespace only")
        return value

class JobCardResult(BaseModel):
    category: CategoryEnum
    priority: PriorityEnum
    reasoning: str

class LLMResponse(BaseModel):
    content: JobCardResult
    model: str
    stubbed: bool = False
    prompt_version: str = "v1"
    duration_ms: float = 0.0
    repair_count: int = 0