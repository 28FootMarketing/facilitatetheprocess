# utils/ollama_bridge.py
import ollama

def call_local_llm(messages, model="mistral"):
    response = ollama.chat(
        model=model,
        messages=messages
    )
    return response['message']['content']
