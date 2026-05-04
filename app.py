import streamlit as st
import json
from config.settings import MODELOS_FREE, TEMPERATURA_DEFAULT
from components.chat import render_chat
from components.comparador import render_comparador
from components.roles import render_roles
from components.analizador import render_analizador
from components.pdf_chat import render_pdf_chat
from components.generador_imagenes import render_generador_imagenes
from utils.helpers import exportar_conversacion, nombre_archivo_chat

st.set_page_config(page_title="AI Studio", page_icon="🧠", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f5f7fa; }
    h1 { color: #1a1a2e; }
    .stChatMessage { background-color: #ffffff; border-radius: 12px; }
    .stSidebar { background-color: #ffffff; }
    div[data-testid="metric-container"] {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar estado
if "messages" not in st.session_state:
    st.session_state.messages = []
if "rol_messages" not in st.session_state:
    st.session_state.rol_messages = []
if "pdf_messages" not in st.session_state:
    st.session_state.pdf_messages = []

# Barra lateral
with st.sidebar:
    st.title("🧠 AI Studio")
    st.divider()

    modo = st.radio("Modo", [
        "💬 Chat",
        "⚡ Comparar modelos",
        "🎭 Roles predefinidos",
        "📊 Analizador de texto",
        "📄 Chat con PDF",
        "🎨 Generador de imágenes",
    ])

    st.divider()

    modelo = st.selectbox("Modelo", MODELOS_FREE)
    temperatura = st.slider("Creatividad", 0.0, 1.0, TEMPERATURA_DEFAULT, 0.1)

    st.divider()

    if st.button("🗑️ Limpiar chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pdf_messages = []
        st.rerun()

    if st.session_state.get("messages"):
        st.download_button(
            "💾 Exportar conversación",
            exportar_conversacion(st.session_state.messages),
            file_name=nombre_archivo_chat(),
            use_container_width=True
        )

# Renderizar modo seleccionado
if modo == "💬 Chat":
    render_chat(modelo, temperatura)
elif modo == "⚡ Comparar modelos":
    render_comparador(temperatura)
elif modo == "🎭 Roles predefinidos":
    render_roles(modelo, temperatura)
elif modo == "📊 Analizador de texto":
    render_analizador(modelo)
elif modo == "📄 Chat con PDF":
    render_pdf_chat(modelo, temperatura)
elif modo == "🎨 Generador de imágenes":
    render_generador_imagenes()