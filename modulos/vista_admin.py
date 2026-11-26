# =====================================================================
# MÓDULO: vista_admin.py
# ACTIVIDAD 4: Panel de control gerencial para el perfil ADMINISTRADOR
# ---------------------------------------------------------------------
# Muestra: KPIs, historial filtrable y análisis de mermas.
# El administrador también puede generar órdenes (acceso total).
# =====================================================================

import streamlit as st

from modulos import datos, vista_cocina


def formato_pesos(valor):
    """Formato chileno: $12.345"""
    return f"${valor:,.0f}".replace(",", ".")


def mostrar():
    st.header("📊 Panel de control – Administrador")

    # Pestañas para ordenar la información
    tab_kpi, tab_historial, tab_mermas, tab_orden = st.tabs(
        ["Resumen", "Historial", "Análisis de mermas", "Nueva orden"]
    )

    ordenes = datos.obtener_ordenes()
    detalle = datos.obtener_detalle()

    # Pestaña para crear órdenes (reutiliza la vista de cocina)
    with tab_orden:
        vista_cocina.mostrar()

    # Si aún no hay órdenes, se avisa y no se calculan métricas
    if ordenes.empty:
        tab_kpi.info("Aún no hay órdenes registradas.")
        return

    # ------------------- 1) RESUMEN EJECUTIVO (KPIs) -------------------
    with tab_kpi:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Servicios realizados", len(ordenes))
        c2.metric("Costo total operación", formato_pesos(ordenes["costo_total"].sum()))
        c3.metric("Pérdida total por merma", formato_pesos(ordenes["perdida_merma_total"].sum()))
        c4.metric("Ingresos proyectados", formato_pesos(ordenes["ingreso_total"].sum()))

    # ------------------- 2) HISTORIAL FILTRABLE ------------------------
    with tab_historial:
        menus = sorted(ordenes["menu"].unique())
        seleccion = st.multiselect("Filtrar por tipo de menú", menus, default=menus)
        filtrado = ordenes[ordenes["menu"].isin(seleccion)]

        st.dataframe(
            filtrado[["id", "fecha", "menu", "comensales", "costo_por_plato",
                      "perdida_merma_total", "precio_venta_plato", "ingreso_total", "usuario"]],
            hide_index=True,
            width="stretch",
        )

        # Desglose de una orden puntual (merma física por ingrediente)
        if not filtrado.empty:
            orden_id = st.selectbox("Ver desglose de la orden N°", filtrado["id"])
            st.dataframe(
                detalle[detalle["orden_id"] == orden_id].drop(columns=["orden_id", "menu"]),
                hide_index=True,
                width="stretch",
            )

    # ------------------- 3) ANÁLISIS DE DESECHOS -----------------------
    with tab_mermas:
        st.subheader("Pérdida por merma según menú ($)")
        por_menu = ordenes.groupby("menu")["perdida_merma_total"].sum().sort_values(ascending=False)
        st.bar_chart(por_menu)

        st.subheader("Pérdida por merma según ingrediente ($)")
        por_ingrediente = detalle.groupby("ingrediente")["perdida_merma"].sum().sort_values(ascending=False)
        st.bar_chart(por_ingrediente)

        # Conclusión automática para apoyar la toma de decisiones
        st.info(
            f"El menú con mayor pérdida es **{por_menu.index[0]}** "
            f"({formato_pesos(por_menu.iloc[0])}) y el ingrediente con mayor "
            f"pérdida es **{por_ingrediente.index[0]}** ({formato_pesos(por_ingrediente.iloc[0])})."
        )
