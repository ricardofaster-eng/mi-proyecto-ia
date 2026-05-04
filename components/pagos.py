import streamlit as st
import stripe
import os
from dotenv import load_dotenv

load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

PLANES = {
    "🥉 Plan Básico": {
        "precio": 999,  # en céntimos = 9.99€
        "descripcion": "100 mensajes al mes",
        "features": ["💬 Chat con IA", "📊 Analizador de texto", "🎭 Roles predefinidos"],
    },
    "🥈 Plan Pro": {
        "precio": 1999,  # en céntimos = 19.99€
        "descripcion": "Mensajes ilimitados",
        "features": ["✅ Todo el Plan Básico", "📄 Chat con PDF", "🎨 Generador de imágenes", "⚡ Comparar modelos"],
    },
    "🥇 Plan Business": {
        "precio": 4999,  # en céntimos = 49.99€
        "descripcion": "Todo incluido + soporte prioritario",
        "features": ["✅ Todo el Plan Pro", "🤖 Agente con herramientas", "🦜 Agente LangChain", "📞 Soporte prioritario"],
    },
}

def crear_sesion_pago(plan_nombre, precio):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": f"AI Studio - {plan_nombre}",
                    },
                    "unit_amount": precio,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url="https://tu-app.streamlit.app?pago=exitoso",
            cancel_url="https://tu-app.streamlit.app?pago=cancelado",
        )
        return session.url
    except Exception as e:
        return None

def render_pagos():
    st.title("💳 Planes y precios")
    st.caption("Elige el plan que mejor se adapte a tus necesidades")

    # Comprobar si volvió de Stripe
    params = st.query_params
    if params.get("pago") == "exitoso":
        st.success("✅ ¡Pago completado! Ya tienes acceso a tu plan.")
    elif params.get("pago") == "cancelado":
        st.warning("❌ Pago cancelado.")

    st.divider()

    cols = st.columns(3)

    for col, (nombre, info) in zip(cols, PLANES.items()):
        with col:
            st.subheader(nombre)
            precio_euros = info["precio"] / 100
            st.markdown(f"## **{precio_euros:.2f}€**/mes")
            st.caption(info["descripcion"])
            st.divider()

            for feature in info["features"]:
                st.write(feature)

            st.divider()

            if st.button(f"Contratar {nombre}", key=nombre, use_container_width=True, type="primary"):
                url = crear_sesion_pago(nombre, info["precio"])
                if url:
                    st.markdown(f'<meta http-equiv="refresh" content="0; url={url}">', unsafe_allow_html=True)
                    st.link_button("👉 Ir al pago", url, use_container_width=True)
                else:
                    st.error("Error al crear sesión de pago")