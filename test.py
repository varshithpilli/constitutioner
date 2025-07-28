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
    "Authorization": "Bearer lol",
    "Content-Type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.json()["choices"][0]["message"]["content"])