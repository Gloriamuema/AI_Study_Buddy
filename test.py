import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
HF_API_URL = "https://api-inference.huggingface.co/models/EleutherAI/gpt-neo-125M"
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

payload = {"inputs": "Generate 1 short flashcard about Python."}

response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=30)
print(response.status_code)
print(response.json())
