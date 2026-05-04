from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Historial de conversación
messages = [
    {"role": "system", "content": "Eres un asistente útil y amigable. Respondes siempre en español."}
]

print("Chatbot iniciado. Escribe 'salir' para terminar.\n")

while True:
    user_input = input("Tú: ")
    
    if user_input.lower() == "salir":
        print("¡Hasta luego!")
        break
    
    # Añadir mensaje del usuario al historial
    messages.append({"role": "user", "content": user_input})
    
    # Llamar a la API
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b:free",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    
    # Añadir respuesta al historial
    messages.append({"role": "assistant", "content": reply})
    
    print(f"\nAsistente: {reply}\n")