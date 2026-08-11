import os
import time
import json
import logging
from typing import Tuple
from groq import Groq, APIConnectionError, APIStatusError, RateLimitError
from dotenv import load_dotenv
from src.llm.schemas import LLMRequest, LLMResponse, JobCardResult, CategoryEnum, PriorityEnum

load_dotenv()
logger = logging.getLogger("uvicorn.error")

PROMPT_FILE_PATH = os.path.join(os.path.dirname(__file__), "../../prompts/v1.txt")

def load_system_prompt() -> str:
    with open(PROMPT_FILE_PATH, "r", encoding="utf-8") as f:
        return f.read().strip()

def call_groq_api_with_retry(messages, model_name: str, timeout: float = 30.0) -> Tuple[str, dict]:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY is not set.")

    client = Groq(api_key=api_key, timeout=timeout)
    
    max_retries = 3
    delay = 1.0

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=messages,
                temperature=0.1
            )
            content = response.choices[0].message.content
            usage = {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
            return content, usage
        except (RateLimitError, APIConnectionError) as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(delay)
            delay *= 2  # Exponential backoff
        except APIStatusError as e:
            # Retry on 5xx server errors, do NOT retry on 400, 401, 403
            if e.status_code >= 500 and attempt < max_retries - 1:
                time.sleep(delay)
                delay *= 2
            else:
                raise e

def generate_llm_response(request: LLMRequest) -> LLMResponse:
    start_time = time.time()
    
    is_enabled = os.getenv("LLM_ENABLED", "true").lower() == "true"
    is_stub = os.getenv("LLM_STUB", "0") == "1"
    model_name = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
    prompt_version = "v1"

    # Rule: LLM_ENABLED=false returns deterministic fallback
    if not is_enabled:
        duration = round((time.time() - start_time) * 1000, 2)
        return LLMResponse(
            content=JobCardResult(
                category=CategoryEnum.OTHER,
                priority=PriorityEnum.LOW,
                reasoning="LLM processing is currently disabled via LLM_ENABLED=false."
            ),
            model="disabled-fallback",
            stubbed=True,
            prompt_version=prompt_version,
            duration_ms=duration,
            repair_count=0
        )

    # Rule: LLM_STUB=1 returns schema-valid response without model call
    if is_stub:
        duration = round((time.time() - start_time) * 1000, 2)
        return LLMResponse(
            content=JobCardResult(
                category=CategoryEnum.DEVELOPMENT,
                priority=PriorityEnum.MEDIUM,
                reasoning=f"Mock offline stub response for input task: '{request.prompt}'"
            ),
            model=model_name,
            stubbed=True,
            prompt_version=prompt_version,
            duration_ms=duration,
            repair_count=0
        )

    system_prompt = load_system_prompt()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": request.prompt}
    ]

    repair_count = 0
    raw_output, usage = call_groq_api_with_retry(messages, model_name)

    # Parse and validate output
    try:
        parsed_json = json.loads(raw_output)
        validated_result = JobCardResult(**parsed_json)
    except Exception as parse_err:
        # Exactly one repair retry
        repair_count = 1
        logger.warning(f"Validation failed. Attempting 1 repair retry. Error: {str(parse_err)}")
        
        repair_messages = messages + [
            {"role": "assistant", "content": raw_output},
            {"role": "user", "content": f"Your output failed validation: {str(parse_err)}. Return valid raw JSON matching the required schema strictly."}
        ]
        
        raw_output, usage = call_groq_api_with_retry(repair_messages, model_name)
        try:
            parsed_json = json.loads(raw_output)
            validated_result = JobCardResult(**parsed_json)
        except Exception as final_err:
            logger.error(f"QUARANTINE LOG: Validation failed after repair attempt for prompt: '{request.prompt}'. Error: {str(final_err)}")
            raise ValueError(f"Model output validation failed: {str(final_err)}")

    duration = round((time.time() - start_time) * 1000, 2)

    # Log operational telemetry
    logger.info(
        f"LLM_CALL | version={prompt_version} | model={model_name} | "
        f"tokens={usage['total_tokens']} | duration_ms={duration} | repair_count={repair_count}"
    )

    return LLMResponse(
        content=validated_result,
        model=model_name,
        stubbed=False,
        prompt_version=prompt_version,
        duration_ms=duration,
        repair_count=repair_count
    )