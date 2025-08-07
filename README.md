
# YashBot 🤖

---

## 🌟 Overview

<b>YashBot</b> is a powerful, modular AI chatbot that can operate in two modes:

- <b>Online Mode</b>: Uses OpenRouter API (Mistral-7B) for cloud-based AI chat.
- <b>Offline Mode</b>: Runs locally with GPT4All (Qwen2-1.5B) for private, no-internet conversations.

It features a modern GUI, a clean CLI, and is designed for both data science and general productivity.

---

## 🚀 Features

- 🔗 <b>Online Mode</b>: Connects to OpenRouter API (Mistral-7B)
- 🖥️ <b>Offline Mode</b>: Uses GPT4All (Qwen2-1.5B) locally
- 🕒 <b>Smart Utilities</b>: Date/time, system info, and more
- 💻 <b>CLI & GUI</b>: Command-line and PyQt5-based GUI
- 🧩 <b>Modular Code</b>: Easy to extend and maintain
- 🎨 <b>Beautiful UI</b>: Dark-themed, modern chat interface

---

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd YashBot
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **(Optional) Set up environment variables**
   - If using environment variables, create a `.env` file and add your API key:
     ```
     OPENROUTER_API_KEY=your_actual_api_key_here
     ```
   - Or, directly insert your API key in `core/online_model.py` as instructed in the code.

4. **Get your OpenRouter API key**
   - Visit [OpenRouter](https://openrouter.ai/keys)
   - Create an account and get your API key

---

## 🛠️ Usage

### Run the Command-Line Version
```bash
python main.py
```

### Run the Modern GUI Version (Recommended)
```bash
python yashbot_gui.py
```

- Choose Online or Offline mode at startup
- Enjoy a visually appealing, dark-themed chat interface

---

## 🖼️ Images & Interface

<p align="center">
  <img src="Pictures/1.png" alt="Chat Interface" width="1000"/>
  <br><i>Online Interface (GUI)</i>
</p>

<p align="center">
  <img src="Pictures/2.png" alt="Project Features" width="1000"/>
  <br><i>Offline Overview</i>
</p>

---

## 📁 Project Structure

```text
YashBot/
├── main.py              # Main application entry point (CLI)
├── yashbot_gui.py       # Modern GUI application (PyQt5)
├── core/
│   ├── online_model.py  # Online AI integration
│   └── offline_model.py # Offline AI integration
├── models/
│   ├── llm_interface.py # GPT4All interface
│   └── *.gguf           # Local AI model files
├── config/              # Configuration files
├── requirements.txt     # Python dependencies
└── .env                 # Environment variables (create this if needed)
```

---

## 📚 Requirements

- Python 3.7+
- Internet connection (for online mode)
- OpenRouter API key (for online mode)
- Local AI model files (for offline mode)

---

## 🔒 Security

- API keys are never committed to git
- `.env` is included in `.gitignore` to prevent accidental commits
- Use `env.example` as a template for your own `.env` file
- You may also insert your API key directly in `core/online_model.py` (see code comments)

---

## 🤝 Contributing

Pull requests, issues, and suggestions are welcome! Please open an issue or PR to contribute.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<p align="center"><b>Built with ❤️ by a Data Analyst exploring AI/ML development</b></p>
