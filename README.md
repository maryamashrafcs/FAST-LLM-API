# FastAPI LLM Service

A production-ready FastAPI application providing structured access to Groq LLM services with offline stubbing support, Pydantic data validation, and automated unit testing.

## Features

- **Groq LLM Integration:** Fast text generation using `llama-3.3-70b-versatile`.
- **Structured Pydantic Schemas:** Strong data validation for inputs and outputs.
- **Offline Stub Mode:** Toggleable offline response mode via environment variables for local testing and offline development.
- **Automated Testing:** Unit test suite using `pytest` and FastAPI `TestClient`.