import streamlit as st
from services.ai_client import get_client
import json
import datetime
import requests

# ── FUNCIONES REALES QUE LA IA PUEDE LLAMAR ──────────────────

def obtener_hora():
    ahora = datetime.datetime.now()
    return f"Son las {ahora.strftime('%H:%M:%S')} del {ahora.strftime('%d/%m/%Y')}"

def calculadora(operacion: str):
    try:
        resultado = eval(operacion)
        return f"{operacion} = {resultado}"
    except:
        return "Error en la operación matemática"

def obtener_tiempo(ciudad: str):
    try:
        url = f"https://wttr.in/{ciudad}?format=3&lang=es"
        response = requests.get(url, timeout=5)
        return response.text
    except:
        return f"No se pudo obtener el tiempo de {ciudad}"

# ── DEFINICIÓN DE HERRAMIENTAS PARA LA IA ────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "obtener_hora",
            "description": "Obtiene la hora y fecha actual del sistema. Úsala SIEMPRE que pregunten qué hora es o qué fecha es hoy.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculadora",
            "description": "Realiza operaciones matemáticas. Úsala SIEMPRE para cualquier cálculo numérico.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operacion": {
                        "type": "string",
                        "description": "La operación matemática. Ej: '1234 * 5678' o '(100 + 50) / 2'"
                    }
                },
                "required": ["operacion"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "obtener_tiempo",
            "description": "Obtiene el tiempo meteorológico actual de una ciudad. Úsala SIEMPRE que pregunten por el tiempo o clima.",
            "parameters": {
                "type": "object",
                "properties": {
                    "ciudad": {
                        "type": "string",
                        "description": "Nombre de la ciudad en inglés. Ej: Madrid, Barcelona, London"
                    }
                },
                "required": ["ciudad"]
            }
        }
    },
]

# ── EJECUTAR FUNCIÓN SEGÚN LO QUE PIDA LA IA ─────────────────

def ejecutar_funcion(nombre, argumentos):
    if nombre == "obtener_hora":
        return obtener_hora()
    elif nombre == "calculadora":
        return calculadora(argumentos.get("operacion", ""))
    elif nombre == "obtener_tiempo":
        return obtener_tiempo(argumentos.get("ciudad", ""))
    return "Función no encontrada"

# ── COMPONENTE STREAMLIT ──────────────────────────────────────

def render_agente(modelo, temperatura):
    st.title("🤖 Agente con herramientas")
    st.caption("La IA decide qué herramientas usar según tu pregunta")

    with st.expander("🛠️ Herramientas disponibles"):
        st.write("- 🕐 **Hora actual** — pregunta qué hora es")
        st.write("- 🧮 **Calculadora** — pregunta cualquier cálculo")
        st.write("- 🌤️ **Tiempo** — pregunta el tiempo de cualquier ciudad")

    if "agente_messages" not in st.session_state:
        st.session_state.agente_messages = []

    if st.button("🔄 Nueva conversación", use_container_width=True):
        st.session_state.agente_messages = []
        st.rerun()

    for msg in st.session_state.agente_messages:
        if msg["role"] in ["user", "assistant"] and msg.get("content"):
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if prompt := st.chat_input("Pregunta algo... Ej: ¿Qué tiempo hace en Madrid?"):
        st.session_state.agente_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        client = get_client()

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = client.chat.completions.create(
                    model="openrouter/auto",
                    messages=[
                        {"role": "system", "content": "Eres un asistente útil con acceso a herramientas. SIEMPRE debes usar las herramientas disponibles cuando el usuario pregunte por la hora, tiempo meteorológico o cálculos matemáticos. NUNCA respondas que no tienes acceso a esa información, usa la herramienta correspondiente. Responde en español."},
                        *st.session_state.agente_messages
                    ],
                    tools=TOOLS,
                    temperature=temperatura,
                )

            mensaje = response.choices[0].message

            # Si la IA quiere usar una herramienta
            if mensaje.tool_calls:
                for tool_call in mensaje.tool_calls:
                    nombre = tool_call.function.name
                    argumentos = json.loads(tool_call.function.arguments)

                    st.info(f"🛠️ Usando herramienta: **{nombre}** con {argumentos}")

                    resultado = ejecutar_funcion(nombre, argumentos)

                    st.session_state.agente_messages.append({
                        "role": "assistant",
                        "content": None,
                        "tool_calls": [tool_call]
                    })
                    st.session_state.agente_messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": resultado
                    })

                # Segunda llamada con el resultado
                with st.spinner("Procesando resultado..."):
                    response2 = client.chat.completions.create(
                        model="openrouter/auto",
                        messages=[
                            {"role": "system", "content": "Eres un asistente útil. Responde en español."},
                            *st.session_state.agente_messages
                        ],
                        temperature=temperatura,
                    )
                reply = response2.choices[0].message.content
            else:
                reply = mensaje.content

            st.write(reply)

        st.session_state.agente_messages.append({"role": "assistant", "content": reply})