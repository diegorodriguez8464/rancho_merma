# =====================================================================
# Prueba del motor de cálculo SIN Supabase ni Streamlit.
# Ejecutar desde la carpeta del proyecto:
#     python -m pruebas.prueba_calculos
# Sirve para verificar a mano los resultados.
# =====================================================================

from modulos.calculos import calcular_ingrediente, calcular_orden, validar_comensales


def ingrediente(id, nombre, costo, unidad, contenido, unidad_contenido, cantidad_base):
    """Arma un ingrediente de receta (base 4 comensales) para las pruebas."""
    return {"id": id, "nombre": nombre, "costo_unitario": costo, "unidad_compra": unidad,
            "contenido": contenido, "unidad_contenido": unidad_contenido,
            "cantidad_base": cantidad_base, "comensales_base": 4}


# Caso 1: Papas para 25 comensales (receta: 6 papas por 4 comensales)
# Necesarias = 6 * 25 / 4 = 37,5 papas. 1 kg = 4 papas -> ceil(9,375) = 10 kg
# Compradas 40 papas -> sobran 2,5 papas = 0,625 kg -> pérdida $625
r = calcular_ingrediente(6 * 25 / 4, 4, 1000)
assert r["unidades_compradas"] == 10
assert r["cantidad_sobrante"] == 2.5
assert r["perdida_merma"] == 625
print("Caso papas 25 comensales:", r)

# Caso 2: menú "Arroz con Pollo y Ensalada" para 4 comensales
ingredientes = [
    ingrediente(3, "Tuto de pollo", 1200, "unidad", 1, "tutos", 4),
    ingrediente(2, "Arroz", 1500, "paquete", 10, "porciones", 4),
    ingrediente(8, "Lechuga", 1000, "unidad", 1, "lechugas", 1),
    ingrediente(10, "Aceite", 1000, "litro", 10, "porciones", 4),
]
orden = calcular_orden(4, ingredientes)
# Costo: 4*1200 + 1500 + 1000 + 1000 = 8.300 -> por plato 2.075
# Venta = 2.075 * 1,25 = 2.593,75 (25 % sobre el costo)
assert orden["costo_total"] == 8300
assert orden["costo_por_plato"] == 2075
assert orden["precio_venta_plato"] == 2593.75
print("\nOrden Arroz con Pollo (4):")
for clave, valor in orden.items():
    if clave != "detalle":
        print(f"  {clave}: {valor}")

# Caso 3: tomates (1 kg = 4 tomates). Receta 3 tomates por 4 comensales
# 8 comensales -> 6 tomates -> 2 kg -> sobran 2 tomates = 0,5 kg -> $750
r = calcular_ingrediente(3 * 8 / 4, 4, 1500)
assert r["unidades_compradas"] == 2 and r["perdida_merma"] == 750

# Caso 4: validaciones
assert validar_comensales(0)[0] is False
assert validar_comensales(-3)[0] is False
assert validar_comensales(None)[0] is False
assert validar_comensales(10)[0] is True

print("\n✔ Todas las pruebas pasaron")
