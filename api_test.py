from httpx import post
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")

base_url = os.getenv("BASE_URL")

payload = {
    "model": "qwen/qwen3-coder:free",
    "messages": [
        {
            "role": "user",
            "content": "How many amendments did the Indian Constitution have as of 2024?"
        }
    ]
}

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

response = post(base_url, json=payload, headers=headers).json()

result = response["choices"][0]["message"]["content"]

print(f"\n\n{result}\n\n")