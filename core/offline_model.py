# core/offline_model.py

import datetime
from models.llm_interface import ask_bot

def offline_chat(prompt: str) -> str:
    """
    Ground the model on today’s date, give it a clear system instruction
    to answer *only* the user’s question, and return just the first line.
    """
    # 1) Fetch real date
    today = datetime.datetime.now().strftime("%Y-%m-%d")

    # 2) Build a mini chat prompt
    system_msg = (
        "You are a concise assistant. Answer only the user's single question "
        "in one sentence and do not continue the conversation."
    )
    user_msg   = f"Today is {today}. {prompt}"
    full_prompt = f"System: {system_msg}\nUser: {user_msg}\nAssistant:"

    # 3) Call GPT4All
    response = ask_bot(full_prompt)

    # 4) Return only the first line (to avoid multi-turn chatter)
    return response.split("\n")[0].strip()

