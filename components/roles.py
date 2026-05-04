import streamlit as st
from services.ai_client import chat_completion

ROLES = {
    "👨‍💻 Programador experto": "Eres un programador experto. Explicas código con claridad, das ejemplos prácticos y sigues buenas prácticas. Respondes en español.",
    "📈 Analista financiero": "Eres un analista financiero experto. Ayudas con inversiones y análisis de mercados. Siempre aclaras que no es consejo financiero oficial. Respondes en español.",
    "🎨 Diseñador creativo": "Eres un diseñador creativo con experiencia en UX/UI. Das ideas innovadoras y ayudas con proyectos creativos. Respondes en español.",
    "🧪 Científico de datos": "Eres un científico de datos experto en Python y machine learning. Explicas conceptos complejos de forma sencilla. Respondes en español.",
    "📝 Redactor profesional": "Eres un redactor profesional. Ayudas a mejorar textos y comunicar ideas con claridad y elegancia. Respondes en español.",
    "🌍 Traductor experto": "Eres un traductor profesional experto en múltiples idiomas. Traduces con precisión manteniendo el tono y contexto originales.",
}

def render_roles(modelo, temperatura):
    st.title("🎭 Asistentes especializados")

    rol = st.selectbox("Elige un asistente", list(ROLES.keys()))
    st.info(f"**Personalidad:** {ROLES[rol]}")

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
                reply = chat_completion(
                    messages=[
                        {"role": "system", "content": ROLES[rol]},
                        *st.session_state.rol_messages
                    ],
                    modelo=modelo,
                    temperatura=temperatura,
                )
            st.write(reply)

        st.session_state.rol_messages.append({"role": "assistant", "content": reply})