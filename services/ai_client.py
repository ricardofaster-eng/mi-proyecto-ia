from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_client():
    return OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
    )

def chat_completion(messages, modelo, temperatura=0.7):
    client = get_client()
    response = client.chat.completions.create(
        model=modelo,
        messages=messages,
        temperature=temperatura,
    )
    return response.choices[0].message.content