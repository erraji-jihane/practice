import requests
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

headers ={
    "x-api-key" : api_key,
    "anthropic-version": "2023-06-01",
    "content-type": "application/json" 
}
body = {
    "model": "claude-haiku-4-5-20251001",
    "max_tokens": 100,
    "messages":[{"role": "user",
                "content": "tell me a joke"}]
}

r = requests.post('https://api.anthropic.com/v1/messages',headers=headers,json=body)

print(r.json())
r.json()['content'][0]['text'] 

