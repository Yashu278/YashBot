# core/online_model.py

import requests

API_KEY = "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"
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

