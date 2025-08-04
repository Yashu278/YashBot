from gpt4all import GPT4All

MODEL_PATH = "/home/yashu278/gpt4all/models/qwen2-1_5b-instruct-q4_0.gguf"

model = GPT4All(model_name=MODEL_PATH)

def ask_bot(prompt):
    with model.chat_session():
        return model.generate(prompt, max_tokens=500)

