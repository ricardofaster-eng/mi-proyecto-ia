import streamlit as st
from services.ai_client import chat_completion
from datetime import datetime

def render_analizador(modelo):
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
                resultado = chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    modelo=modelo,
                    temperatura=0.3,
                )

            st.divider()
            st.subheader("📊 Resultados")
            st.write(resultado)

            st.download_button(
                "💾 Descargar análisis",
                resultado,
                file_name=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                use_container_width=True
            )