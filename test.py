import requests

url = "https://openrouter.ai/api/v1/chat/completions"

payload = {
    "model": "mistralai/mistral-small-3.2-24b-instruct:free",
    "messages": [
        {
            "role": "system",
            "content": "You are a philosopher"
        },
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ]
}
headers = {
    "Authorization": "Bearer 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",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json()["choices"][0]["message"]["content"])