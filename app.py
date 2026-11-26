# =====================================================================
# SISTEMA DE INVENTARIO DE ALIMENTOS, CONTROL Y GESTIÓN DE MERMAS
# ---------------------------------------------------------------------
# Alumno     : Teniente Diego [APELLIDO]
# Curso      : Programación Avanzada – I CRIM Sistemas de Armas
# Profesor   : Dr. Carlos Santibáñez Rodríguez
# Evaluación : Solemne N°3
# Institución: Academia Politécnica Militar (ACAPOMIL)
# Fecha      : 26-11-2026
#
# Librerías utilizadas:
#   - streamlit : interfaz web (formularios, tablas, métricas, gráficos)
#   - supabase  : conexión a la base de datos PostgreSQL en la nube
#   - pandas    : manejo de tablas (filtros, agrupaciones, totales)
#   - math      : math.ceil para redondear hacia arriba (indivisibilidad)
#
# Estructura del proyecto (separación por responsabilidad):
#   app.py                 -> punto de entrada, login y navegación por rol
#   modulos/conexion.py    -> conexión segura a Supabase (st.secrets)
#   modulos/datos.py       -> consultas e inserciones en la base de datos
#   modulos/calculos.py    -> motor de cálculo (cantidades, merma, costos)
#   modulos/vista_cocina.py-> pantalla del perfil cocina
#   modulos/vista_admin.py -> panel del perfil administrador
#   sql/                   -> scripts para crear y poblar la base de datos
#
# Ejecución (Windows):  python -m streamlit run app.py
# =====================================================================

import streamlit as st

from modulos import datos, vista_admin, vista_cocina

st.set_page_config(page_title="Control de Alimentos y Mermas", page_icon="🍽️", layout="wide")

# ---------------------------------------------------------------------
# Estado de la sesión: se guarda quién inició sesión y con qué rol.
# st.session_state mantiene los datos entre recargas de la página.
# ---------------------------------------------------------------------
if "rol" not in st.session_state:
    st.session_state.rol = None
    st.session_state.usuario = None


def pantalla_login():
    """Formulario de identificación de usuario."""
    st.title("🍽️ Control de Alimentos y Mermas")
    with st.form("login"):
        usuario = st.text_input("Usuario")
        clave = st.text_input("Contraseña", type="password")
        ingresar = st.form_submit_button("Ingresar")

    if ingresar:
        rol = datos.validar_usuario(usuario.strip(), clave)
        if rol:
            st.session_state.rol = rol
            st.session_state.usuario = usuario.strip()
            st.rerun()  # Recarga la página para mostrar la vista del rol
        else:
            st.error("Usuario o contraseña incorrectos.")


def cerrar_sesion():
    st.session_state.rol = None
    st.session_state.usuario = None


# ---------------------------------------------------------------------
# Navegación según rol (control de acceso)
#   - Sin sesión     -> login
#   - cocina         -> solo vista operativa (sin costos)
#   - administrador  -> panel completo
# ---------------------------------------------------------------------
if st.session_state.rol is None:
    pantalla_login()
else:
    st.sidebar.write(f"👤 **{st.session_state.usuario}**")
    st.sidebar.write(f"Rol: {st.session_state.rol}")
    st.sidebar.button("Cerrar sesión", on_click=cerrar_sesion)

    if st.session_state.rol == "cocina":
        vista_cocina.mostrar()
    elif st.session_state.rol == "administrador":
        vista_admin.mostrar()
