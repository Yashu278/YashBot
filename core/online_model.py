# core/online_model.py

import requests

 # Insert your API key here
API_KEY = "INSERT_YOUR_API_KEY_HERE"  # <-- Replace with your actual API key
MODEL   = "mistralai/mistral-7b-instruct:free"

def online_chat(prompt):
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

