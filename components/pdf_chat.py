import streamlit as st
import PyPDF2
import io
from services.ai_client import chat_completion

def extraer_texto_pdf(archivo):
    reader = PyPDF2.PdfReader(io.BytesIO(archivo.read()))
    texto = ""
    for pagina in reader.pages:
        texto += pagina.extract_text() + "\n"
    return texto

def render_pdf_chat(modelo, temperatura):
    st.title("📄 Chat con tu PDF")
    st.caption("Sube un PDF y hazle preguntas")

    archivo = st.file_uploader("Sube tu PDF", type=["pdf"])

    if archivo:
        with st.spinner("Leyendo PDF..."):
            texto = extraer_texto_pdf(archivo)
        
        st.success(f"✅ PDF cargado: {len(texto)} caracteres leídos")
        
        with st.expander("Ver contenido del PDF"):
            st.text(texto[:2000] + "..." if len(texto) > 2000 else texto)

        if "pdf_messages" not in st.session_state:
            st.session_state.pdf_messages = []

        if st.button("🔄 Nueva conversación", use_container_width=True):
            st.session_state.pdf_messages = []
            st.rerun()

        for msg in st.session_state.pdf_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        if prompt := st.chat_input("Hazle una pregunta al PDF..."):
            st.session_state.pdf_messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Analizando..."):
                    reply = chat_completion(
                        messages=[
                            {"role": "system", "content": f"""Eres un asistente experto en analizar documentos. 
El usuario te ha proporcionado el siguiente documento PDF:

{texto[:8000]}

Responde las preguntas basándote únicamente en el contenido del documento. Responde en español."""},
                            *st.session_state.pdf_messages
                        ],
                        modelo=modelo,
                        temperatura=temperatura,
                    )
                st.write(reply)

            st.session_state.pdf_messages.append({"role": "assistant", "content": reply})