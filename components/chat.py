import streamlit as st
from services.ai_client import chat_completion
from config.settings import SYSTEM_PROMPT_DEFAULT

def render_chat(modelo, temperatura):
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
                reply = chat_completion(
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT_DEFAULT},
                        *st.session_state.messages
                    ],
                    modelo=modelo,
                    temperatura=temperatura,
                )
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})