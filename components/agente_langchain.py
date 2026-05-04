import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
import os
import datetime

load_dotenv()

# ── HERRAMIENTAS ──────────────────────────────────────────────

@tool
def obtener_hora(query: str = "") -> str:
    """Obtiene la hora y fecha actual del sistema."""
    ahora = datetime.datetime.now()
    return f"Son las {ahora.strftime('%H:%M:%S')} del {ahora.strftime('%d/%m/%Y')}"

@tool
def calculadora(operacion: str) -> str:
    """Realiza operaciones matemáticas. Ej: '1234 * 5678'"""
    try:
        resultado = eval(operacion)
        return f"{operacion} = {resultado}"
    except Exception as e:
        return f"Error: {str(e)}"

search = DuckDuckGoSearchRun()
TOOLS = [obtener_hora, calculadora, search]

# ── CREAR AGENTE ──────────────────────────────────────────────

def crear_agente():
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model="openai/gpt-oss-120b:free",
        temperature=0.3,
    )
    return create_react_agent(
        model=llm,
        tools=TOOLS,
        prompt="Eres un asistente útil. SIEMPRE usa las herramientas disponibles para hora, cálculos y búsquedas. Responde en español.",
    )

# ── COMPONENTE STREAMLIT ──────────────────────────────────────

def render_agente_langchain():
    st.title("🦜 Agente LangChain")
    st.caption("Agente con búsqueda en internet, calculadora y más")

    with st.expander("🛠️ Herramientas disponibles"):
        st.write("- 🕐 **Hora actual**")
        st.write("- 🧮 **Calculadora**")
        st.write("- 🔍 **Búsqueda en internet** con DuckDuckGo")

    if "langchain_messages" not in st.session_state:
        st.session_state.langchain_messages = []
    if "langchain_history" not in st.session_state:
        st.session_state.langchain_history = []

    if st.button("🔄 Nueva conversación", use_container_width=True):
        st.session_state.langchain_messages = []
        st.session_state.langchain_history = []
        st.rerun()

    for msg in st.session_state.langchain_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Pregunta algo... Ej: ¿Cuáles son las últimas noticias de IA?"):
        st.session_state.langchain_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("El agente está trabajando..."):
                try:
                    agente = crear_agente()
                    
                    historial = st.session_state.langchain_history + [
                        HumanMessage(content=prompt)
                    ]
                    
                    resultado = agente.invoke({"messages": historial})
                    reply = resultado["messages"][-1].content

                    st.session_state.langchain_history.append(HumanMessage(content=prompt))
                    st.session_state.langchain_history.append(AIMessage(content=reply))

                except Exception as e:
                    reply = f"Error: {str(e)}"

            st.write(reply)

        st.session_state.langchain_messages.append({"role": "assistant", "content": reply})