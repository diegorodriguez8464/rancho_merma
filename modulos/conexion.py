# =====================================================================
# MÓDULO: conexion.py
# ACTIVIDAD 5: Manejo seguro de credenciales
# ---------------------------------------------------------------------
# Las llaves NO se escriben en el código. Se leen desde
# .streamlit/secrets.toml (archivo que NO se sube a GitHub,
# está incluido en .gitignore).
# =====================================================================

import streamlit as st
from supabase import create_client


@st.cache_resource  # Se crea una sola conexión y se reutiliza (más rápido)
def obtener_cliente():
    url = st.secrets["SUPABASE_URL"]
    llave = st.secrets["SUPABASE_KEY"]
    return create_client(url, llave)
