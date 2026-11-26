# =====================================================================
# MÓDULO: datos.py
# Capa de acceso a datos: TODAS las consultas a Supabase están aquí.
# Decisión: si cambia la base de datos, solo se modifica este archivo;
# las vistas (cocina/admin) no saben cómo se guardan los datos.
# =====================================================================

import pandas as pd
from modulos.conexion import obtener_cliente


# ---------------------------- USUARIOS -------------------------------
def validar_usuario(usuario, clave):
    """Llama a la función SQL validar_usuario. Retorna el rol o None."""
    sb = obtener_cliente()
    respuesta = sb.rpc("validar_usuario", {"p_usuario": usuario, "p_clave": clave}).execute()
    return respuesta.data  # 'cocina', 'administrador' o None


# ---------------------------- CATÁLOGO -------------------------------
def obtener_recetas():
    """Lista de recetas (id y nombre) ordenadas alfabéticamente."""
    sb = obtener_cliente()
    return sb.table("recetas").select("id, nombre").order("nombre").execute().data


def obtener_ingredientes_receta(receta_id):
    """Ingredientes de una receta: cantidad de la receta, costo y contenido."""
    sb = obtener_cliente()
    filas = (
        sb.table("receta_ingredientes")
        .select("cantidad_base, recetas(comensales_base), "
                "ingredientes(id, nombre, costo_unitario, unidad_compra, contenido, unidad_contenido)")
        .eq("receta_id", receta_id)
        .execute()
        .data
    )
    # Supabase devuelve receta e ingrediente anidados: se "aplana" la lista
    return [
        {
            "id": f["ingredientes"]["id"],
            "nombre": f["ingredientes"]["nombre"],
            "costo_unitario": float(f["ingredientes"]["costo_unitario"]),
            "unidad_compra": f["ingredientes"]["unidad_compra"],
            "contenido": float(f["ingredientes"]["contenido"]),
            "unidad_contenido": f["ingredientes"]["unidad_contenido"],
            "cantidad_base": float(f["cantidad_base"]),
            "comensales_base": f["recetas"]["comensales_base"],
        }
        for f in filas
    ]


# ---------------------------- ÓRDENES --------------------------------
def guardar_orden(receta_id, comensales, resultado, usuario):
    """Guarda la orden y su detalle. Retorna el id de la orden creada."""
    sb = obtener_cliente()

    # 1) Encabezado de la orden
    orden = {
        "receta_id": receta_id,
        "comensales": comensales,
        "costo_total": resultado["costo_total"],
        "costo_por_plato": resultado["costo_por_plato"],
        "precio_venta_plato": resultado["precio_venta_plato"],
        "ingreso_total": resultado["ingreso_total"],
        "perdida_merma_total": resultado["perdida_merma_total"],
        "usuario": usuario,
    }
    orden_id = sb.table("ordenes").insert(orden).execute().data[0]["id"]

    # 2) Detalle por ingrediente (se inserta todo en una sola llamada)
    detalle = [
        {
            "orden_id": orden_id,
            "ingrediente_id": d["ingrediente_id"],
            "unidades_compradas": d["unidades_compradas"],
            "cantidad_necesaria": d["cantidad_necesaria"],
            "cantidad_sobrante": d["cantidad_sobrante"],
            "merma_fraccion": d["merma_fraccion"],
            "costo": d["costo"],
            "perdida_merma": d["perdida_merma"],
        }
        for d in resultado["detalle"]
    ]
    sb.table("orden_detalle").insert(detalle).execute()
    return orden_id


def obtener_ordenes():
    """Historial de órdenes como DataFrame (vista v_ordenes)."""
    sb = obtener_cliente()
    datos = sb.table("v_ordenes").select("*").order("fecha", desc=True).execute().data
    return pd.DataFrame(datos)


def obtener_detalle():
    """Detalle de insumos de todas las órdenes (vista v_detalle)."""
    sb = obtener_cliente()
    datos = sb.table("v_detalle").select("*").execute().data
    return pd.DataFrame(datos)
