import streamlit as st
import requests
from urllib.parse import quote

def render_generador_imagenes():
    st.title("🎨 Generador de imágenes con IA")
    st.caption("Describe lo que quieres ver y la IA lo creará")

    prompt = st.text_area("Describe la imagen", height=100,
        placeholder="Ej: Un gato astronauta flotando en el espacio, estilo realista")

    estilo = st.selectbox("Estilo", [
        "Ninguno",
        "Photorealistic",
        "Oil painting",
        "Anime",
        "Watercolor",
        "Digital art",
        "Pixel art",
        "Pencil sketch",
    ])

    negativo = st.text_input("Qué NO quieres ver",
        placeholder="Ej: personas, texto, colores oscuros")

    ancho, alto = st.select_slider("Tamaño",
        options=[512, 768, 1024],
        value=(1024, 1024)
    )

    if st.button("🎨 Generar imagen", use_container_width=True, type="primary"):
        if prompt:
            prompt_final = prompt
            if estilo != "Ninguno":
                prompt_final += f", {estilo} style"
            if negativo:
                prompt_final += f". Avoid: {negativo}"

            url = f"https://image.pollinations.ai/prompt/{quote(prompt_final)}?width={ancho}&height={alto}&nologo=true"

            with st.spinner("Generando imagen... puede tardar unos segundos"):
                try:
                    response = requests.get(url, timeout=60)
                    if response.status_code == 200:
                        st.image(response.content, caption=prompt, use_column_width=True)
                        st.success("✅ Imagen generada")
                        st.download_button(
                            "💾 Descargar imagen",
                            response.content,
                            file_name="imagen_ia.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.error(f"Error al generar: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")