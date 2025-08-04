#!/usr/bin/env python3
import sys
import datetime

from core.online_model import online_chat
from core.offline_model import offline_chat
from dotenv import load_dotenv
load_dotenv()

# ——— Model Selection ———
print("🤖 Choose your AI model:")
print("1. Online (requires Internet)")
print("2. Offline (local GPT4All)")
mode = input("Enter 1 or 2: ").strip()
chat_model = online_chat if mode == "1" else offline_chat
print(f"✅ Using {'Online' if mode == '1' else 'Offline'} mode.\n")

# ——— Chat Loop ———
def main():
    print("🤖 YashBot is ready! Type 'exit' or 'quit' to stop.")
    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ("exit", "quit"):
                print("👋 Exiting YashBot. Goodbye!")
                break

            if any(keyword in user_input.lower() for keyword in ("date", "today", "time", "now")):
                now = datetime.datetime.now()
                print("YashBot:", now.strftime("%A, %B %d, %Y at %H:%M:%S"))
                continue

            response = chat_model(user_input)
            print("YashBot:", response)

    except KeyboardInterrupt:
        print("\n👋 KeyboardInterrupt received. Exiting YashBot.")

if __name__ == "__main__":
    main()

