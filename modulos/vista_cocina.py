# =====================================================================
# MÓDULO: vista_cocina.py
# ACTIVIDAD 3: Interfaz operativa para el perfil COCINA
# ---------------------------------------------------------------------
# Regla clave: el usuario cocina SOLO ve ingredientes y cantidades.
# NO se muestra ningún costo, pérdida ni precio (aunque se calculan
# y se guardan en Supabase para el administrador).
# =====================================================================

import pandas as pd
import streamlit as st

from modulos import datos
from modulos.calculos import calcular_orden, validar_comensales


def mostrar():
    st.header("🍳 Solicitud de servicio – Cocina")

    recetas = datos.obtener_recetas()
    # Diccionario nombre -> id para usar en el selectbox
    opciones = {r["nombre"]: r["id"] for r in recetas}

    # Formulario: los datos se envían solo al presionar el botón
    with st.form("form_solicitud"):
        menu = st.selectbox("Tipo de menú", list(opciones.keys()))
        # value=0 obliga al usuario a escribir un valor; se valida abajo
        comensales = st.number_input("Cantidad de comensales", value=0, step=1)
        enviar = st.form_submit_button("Generar orden de preparación")

    if not enviar:
        return

    # Validación: no nulos, negativos ni cero
    es_valido, mensaje = validar_comensales(comensales)
    if not es_valido:
        st.error(mensaje)
        return

    comensales = int(comensales)
    receta_id = opciones[menu]

    # Cálculo completo (incluye costos, que NO se muestran aquí)
    ingredientes = datos.obtener_ingredientes_receta(receta_id)
    resultado = calcular_orden(comensales, ingredientes)

    # Guardado automático en Supabase
    try:
        orden_id = datos.guardar_orden(receta_id, comensales, resultado, st.session_state.usuario)
        st.success(f"Orden N° {orden_id} registrada correctamente.")
    except Exception as error:
        st.error(f"No se pudo guardar la orden: {error}")
        return

    # Orden de preparación: solo ingredientes y cantidades (sin montos)
    #   - "Retirar": unidades completas que se sacan de bodega
    #   - "Usar en la preparación": cantidad exacta según la receta
    st.subheader(f"Orden de preparación: {menu} ({comensales} comensales)")
    tabla = pd.DataFrame(
        [
            {
                "Ingrediente": d["nombre"],
                "Retirar": f'{d["unidades_compradas"]} {d["unidad_compra"]}',
                # :g quita decimales innecesarios; se usa coma decimal (formato chileno)
                "Usar en la preparación": f'{d["cantidad_necesaria"]:g} {d["unidad_contenido"]}'.replace(".", ","),
            }
            for d in resultado["detalle"]
        ]
    )
    st.table(tabla)
