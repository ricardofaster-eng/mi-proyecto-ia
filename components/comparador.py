import streamlit as st
from services.ai_client import chat_completion
from config.settings import MODELOS_FREE

def render_comparador(temperatura):
    st.title("⚡ Comparar modelos en paralelo")
    st.caption("La misma pregunta a varios modelos distintos")

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
                            reply = chat_completion(
                                messages=[{"role": "user", "content": pregunta}],
                                modelo=mod,
                                temperatura=temperatura,
                            )
                            st.info(reply)
                        except Exception as e:
                            st.error(f"Error: {str(e)[:120]}")