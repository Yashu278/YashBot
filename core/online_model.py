# core/online_model.py

import requests
import os

# Get API key from environment variable
API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL   = "mistralai/mistral-7b-instruct:free"

def online_chat(prompt):
    if not API_KEY:
        return "⚠ Error: OPENROUTER_API_KEY environment variable not set. Please add your API key to .env file."
    
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
        "HTTP-Referer":  "https://yashbot.local",
        "X-Title":       "YashBot CLI"
    }
    data = {
        "model":       MODEL,
        "messages": [
            {"role": "system", "content": "You are YashBot, a helpful assistant."},
            {"role": "user",   "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        r = requests.post(url, headers=headers, json=data)
        r.raise_for_status()
        j = r.json()
        return j["choices"][0]["message"]["content"]
    except Exception as e:
        return f"⚠ Error in online response: {e}"

