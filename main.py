from openai import OpenAI
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Conectar con OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Hacer una pregunta a un modelo de IA
response = client.chat.completions.create(
    model="openai/gpt-oss-120b:free",
    messages=[
        {"role": "user", "content": "Hola, ¿qué eres y qué puedes hacer?"}
    ]
)

print(response.choices[0].message.content)