# 🤖 YashBot – Your Personal AI Assistant (Offline + Online)

YashBot is a privacy-first AI assistant built in Python. It can run **fully offline** using local models (like GPT4All, Mistral, Phi-3) and can also switch to **online models** (via OpenRouter) when internet is available. Designed for CLI usage with smart features and a modular structure.

## 🚀 Features

- ✅ Launch desktop apps with fuzzy matching (even with typos)
- ✅ Explain terminal commands in plain language
- ✅ Manage files: detect low storage, rename, delete, etc.
- ✅ Answer coding & general questions using offline LLMs
- ✅ Use OpenRouter for powerful cloud models (optional)
- ✅ Modular structure (easy to extend)
- ✅ Offline-first, privacy-respecting & FREE

## 📂 Project Structure

```
YashBot/
├── main.py             # CLI entry point
├── config/             # Config files and helpers
├── core/               # AI logic and task handlers
│   ├── local_model.py
│   ├── online_model.py
│   └── ...
├── models/             # Local .gguf models (not tracked in git)
├── test_api.py         # Quick test script for OpenRouter
└── .env                # API keys (not tracked)
```

## 🛠️ Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

> 📌 You'll also need to manually download and place `.gguf` model files in the `models/` folder.

## 🔐 Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openrouter_api_key_here
```

> This is used for online responses through OpenRouter. Keep this file **private**.

## 🧠 Models Used

* **Offline (GPT4All-compatible)**: Mistral, Phi-3, etc.
* **Online (via OpenRouter)**: mistralai/mistral-7b-instruct:free

## ✅ Example Usage

Run the assistant:

```bash
python main.py
```

And try commands like:

```bash
> open chrome
> explain chmod -R 755 dir
> low storage
> debug this python code: ...
```

## 🛡️ Privacy & Offline Mode

YashBot is designed to **respect your data**. It works 100% offline unless you explicitly use the online mode (which still avoids OpenAI directly by using OpenRouter).

## 📌 TODO (Coming Soon)

* [ ] GUI interface (optional)
* [ ] Voice control & text-to-speech
* [ ] Background task scheduling
* [ ] Auto-updater for models

## 🧑‍💻 Author

**Yashdeep Saxena**  
Student – B.Tech AI & Data Science  
GitHub: [@Yashu278](https://github.com/Yashu278)  
LinkedIn: [Yashdeep Saxena](https://www.linkedin.com/in/yashdeep-saxena-3a6914295/)

## 📜 License

MIT License – Feel free to use, modify, and share. Give credit where due.

---
ts.txt` next?
