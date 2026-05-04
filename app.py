import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

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

MODELOS_FREE = [
    "openrouter/free",
    "openai/gpt-oss-120b:free",
    "meta-llama/llama-3.1-8b-instruct:free",
    "google/gemma-3-12b-it:free",
    "google/gemma-3-1b-it:free",
    "deepseek/deepseek-r1:free",
    "mistralai/mistral-small-3.1-24b-instruct:free",
    "qwen/qwen2.5-vl-72b-instruct:free",
]

with st.sidebar:
    st.title("🧠 AI Studio")
    st.divider()

    modo = st.radio("Modo", [
        "💬 Chat",
        "⚡ Comparar modelos",
        "🎭 Roles predefinidos",
        "📊 Analizador de texto",
    ])

    st.divider()

    modelo = st.selectbox("Modelo", MODELOS_FREE)
    temperatura = st.slider("Creatividad", 0.0, 1.0, 0.7, 0.1,
        help="0 = preciso, 1 = creativo")

    st.divider()

    if st.button("🗑️ Limpiar chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    if st.session_state.get("messages"):
        st.download_button(
            "💾 Exportar conversación",
            json.dumps(st.session_state.messages, ensure_ascii=False, indent=2),
            file_name=f"chat_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            use_container_width=True
        )

if "messages" not in st.session_state:
    st.session_state.messages = []
if "rol_messages" not in st.session_state:
    st.session_state.rol_messages = []

# ── CHAT ──────────────────────────────────────────────────────
if modo == "💬 Chat":
    st.title("💬 Chat con IA")

    col1, col2, col3 = st.columns(3)
    col1.metric("Mensajes", len(st.session_state.messages))
    col2.metric("Modelo", modelo.split("/")[-1][:22])
    col3.metric("Creatividad", temperatura)
    st.divider()

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input("Escribe tu mensaje..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": "Eres un asistente útil. Respondes en español."},
                        *st.session_state.messages
                    ],
                    temperature=temperatura,
                )
            reply = response.choices[0].message.content
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})

# ── COMPARAR MODELOS ──────────────────────────────────────────
elif modo == "⚡ Comparar modelos":
    st.title("⚡ Comparar modelos en paralelo")
    st.caption("La misma pregunta a 3 modelos distintos")

    pregunta = st.text_area("Tu pregunta", height=100,
        placeholder="Ej: Explícame qué es la inteligencia artificial")

    modelos_comparar = st.multiselect("Modelos a comparar", MODELOS_FREE,
        default=MODELOS_FREE[1:4])

    if st.button("🚀 Comparar", use_container_width=True, type="primary"):
        if pregunta and modelos_comparar:
            cols = st.columns(len(modelos_comparar))
            for col, mod in zip(cols, modelos_comparar):
                with col:
                    st.subheader(f"🤖 {mod.split('/')[-1][:22]}")
                    with st.spinner("Generando..."):
                        try:
                            resp = client.chat.completions.create(
                                model=mod,
                                messages=[{"role": "user", "content": pregunta}],
                                temperature=temperatura,
                            )
                            st.info(resp.choices[0].message.content)
                        except Exception as e:
                            st.error(f"Error: {str(e)[:120]}")

# ── ROLES ─────────────────────────────────────────────────────
elif modo == "🎭 Roles predefinidos":
    st.title("🎭 Asistentes especializados")

    roles = {
        "👨‍💻 Programador experto": "Eres un programador experto. Explicas código con claridad, das ejemplos prácticos y sigues buenas prácticas. Respondes en español.",
        "📈 Analista financiero": "Eres un analista financiero experto. Ayudas con inversiones y análisis de mercados. Siempre aclaras que no es consejo financiero oficial. Respondes en español.",
        "🎨 Diseñador creativo": "Eres un diseñador creativo con experiencia en UX/UI. Das ideas innovadoras y ayudas con proyectos creativos. Respondes en español.",
        "🧪 Científico de datos": "Eres un científico de datos experto en Python y machine learning. Explicas conceptos complejos de forma sencilla. Respondes en español.",
        "📝 Redactor profesional": "Eres un redactor profesional. Ayudas a mejorar textos y comunicar ideas con claridad y elegancia. Respondes en español.",
        "🌍 Traductor experto": "Eres un traductor profesional experto en múltiples idiomas. Traduces con precisión manteniendo el tono y contexto originales.",
    }

    rol = st.selectbox("Elige un asistente", list(roles.keys()))
    st.info(f"**Personalidad:** {roles[rol]}")

    if st.button("🔄 Nueva conversación", use_container_width=True):
        st.session_state.rol_messages = []
        st.rerun()

    for msg in st.session_state.rol_messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    if prompt := st.chat_input(f"Habla con {rol}..."):
        st.session_state.rol_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Pensando..."):
                response = client.chat.completions.create(
                    model=modelo,
                    messages=[
                        {"role": "system", "content": roles[rol]},
                        *st.session_state.rol_messages
                    ],
                    temperature=temperatura,
                )
            reply = response.choices[0].message.content
            st.write(reply)

        st.session_state.rol_messages.append({"role": "assistant", "content": reply})

# ── ANALIZADOR ────────────────────────────────────────────────
elif modo == "📊 Analizador de texto":
    st.title("📊 Analizador de texto con IA")

    texto = st.text_area("Pega aquí tu texto", height=200,
        placeholder="Email, artículo, contrato, código...")

    tipo_analisis = st.multiselect("¿Qué quieres analizar?", [
        "📝 Resumen",
        "😊 Sentimiento y tono",
        "🔑 Palabras clave",
        "✅ Puntos fuertes y débiles",
        "🌍 Traducir al inglés",
        "✍️ Mejorar el texto",
        "❓ Preguntas frecuentes que generaría este texto",
    ], default=["📝 Resumen", "😊 Sentimiento y tono"])

    if st.button("🔍 Analizar", use_container_width=True, type="primary"):
        if texto and tipo_analisis:
            prompt = f"""Analiza el siguiente texto y proporciona exactamente estos análisis:
{chr(10).join(tipo_analisis)}

Texto:
{texto}

Responde en español con secciones claramente separadas."""

            with st.spinner("Analizando..."):
                response = client.chat.completions.create(
                    model=modelo,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                )

            resultado = response.choices[0].message.content
            st.divider()
            st.subheader("📊 Resultados")
            st.write(resultado)

            st.download_button(
                "💾 Descargar análisis",
                resultado,
                file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                use_container_width=True
            )