# =====================================================================
# MÓDULO: calculos.py
# ACTIVIDAD 2: Motor de cálculo y gestión de mermas
# ---------------------------------------------------------------------
# Este módulo NO usa Streamlit ni Supabase: solo matemática.
# Decisión: separar la lógica de cálculo permite probarla sola
# (ver pruebas/prueba_calculos.py) y reutilizarla en cualquier vista.
#
# MODELO DE CÁLCULO:
#   1) La receta indica la cantidad de cada ingrediente para su base
#      de comensales (4). Se escala en forma proporcional:
#         cantidad necesaria = cantidad_base * comensales / comensales_base
#   2) Cada unidad de compra trae un "contenido" medido en la misma
#      unidad de la receta. Ej: 1 kg de papas = 4 papas,
#      1 paquete de arroz = 10 porciones, 1 empaque = 12 huevos.
#   3) Como los productos son INDIVISIBLES y NO se guardan, se compran
#      unidades completas (math.ceil) y lo que sobra es MERMA.
# =====================================================================

import math

# Margen de ganancia solicitado en el enunciado (25 %)
MARGEN_GANANCIA = 0.25


def validar_comensales(valor):
    """Valida que la cantidad de comensales no sea nula, negativa ni cero.
    Retorna (True, "") si es válida, o (False, mensaje) si no lo es."""
    if valor is None:
        return False, "Debe ingresar la cantidad de comensales."
    if not float(valor).is_integer():
        return False, "La cantidad de comensales debe ser un número entero."
    if valor <= 0:
        return False, "La cantidad de comensales debe ser mayor a cero."
    return True, ""


def calcular_ingrediente(cantidad_necesaria, contenido, costo_unitario):
    """Calcula compra, merma y pérdida de UN ingrediente.

    cantidad_necesaria: lo que pide la receta ya escalada (ej: 37.5 papas)
    contenido: cuánto trae 1 unidad de compra (ej: 4 papas por kg)
    """
    # 1) Unidades a comprar: redondeo hacia arriba (producto indivisible).
    #    round(..., 6) evita errores de decimales, ej: 2.0000000001 -> 2
    unidades = math.ceil(round(cantidad_necesaria / contenido, 6))

    # 2) Cantidad comprada vs. cantidad usada (en unidades de la receta)
    cantidad_comprada = unidades * contenido
    cantidad_sobrante = cantidad_comprada - cantidad_necesaria

    # 3) Merma física: fracción de unidad de compra que no se usa
    merma_fraccion = cantidad_sobrante / contenido

    # 4) Valorización: costo de lo comprado y pérdida en pesos por la merma
    costo = unidades * costo_unitario
    perdida = merma_fraccion * costo_unitario

    return {
        "unidades_compradas": unidades,
        "cantidad_necesaria": round(cantidad_necesaria, 2),
        "cantidad_sobrante": round(cantidad_sobrante, 2),
        "merma_fraccion": round(merma_fraccion, 4),
        "costo": round(costo, 2),
        "perdida_merma": round(perdida, 2),
    }


def calcular_orden(comensales, ingredientes):
    """Calcula la orden completa de un menú.

    ingredientes: lista de diccionarios con las llaves
        id, nombre, unidad_compra, contenido, unidad_contenido,
        costo_unitario, cantidad_base, comensales_base
    """
    detalle = []
    for ing in ingredientes:
        # Escalar la receta a la cantidad de comensales solicitada
        cantidad_necesaria = ing["cantidad_base"] * comensales / ing["comensales_base"]

        resultado = calcular_ingrediente(cantidad_necesaria, ing["contenido"], ing["costo_unitario"])
        # Se agregan los datos del ingrediente al resultado
        resultado["ingrediente_id"] = ing["id"]
        resultado["nombre"] = ing["nombre"]
        resultado["unidad_compra"] = ing["unidad_compra"]
        resultado["unidad_contenido"] = ing["unidad_contenido"]
        detalle.append(resultado)

    # Totales de la orden
    costo_total = sum(d["costo"] for d in detalle)
    perdida_total = sum(d["perdida_merma"] for d in detalle)

    # Costo real por plato = costo total de productos indivisibles / comensales
    costo_por_plato = costo_total / comensales

    # Precio de venta = costo por plato + 25 % de ganancia SOBRE EL COSTO
    # (markup): precio = costo * 1,25. Ej: costo $2.000 -> venta $2.500
    precio_venta = costo_por_plato * (1 + MARGEN_GANANCIA)

    return {
        "detalle": detalle,
        "costo_total": round(costo_total, 2),
        "perdida_merma_total": round(perdida_total, 2),
        "costo_por_plato": round(costo_por_plato, 2),
        "precio_venta_plato": round(precio_venta, 2),
        "ingreso_total": round(precio_venta * comensales, 2),
    }
