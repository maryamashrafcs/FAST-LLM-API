import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model=os.getenv("LLM_MODEL", "llama-3.3-70b-versatile"),
    messages=[{"role": "user", "content": "Reply with exactly the word: ready"}]
)

print(response.choices[0].message.content)