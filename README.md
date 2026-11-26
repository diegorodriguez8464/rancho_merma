# Rancho Merma – Control de Alimentos y Gestión de Mermas

Aplicación web para planificar la preparación de menús en una cocina institucional. A partir del menú elegido y la cantidad de comensales, el sistema calcula los productos que hay que usar, la merma que se genera, la pérdida económica asociada, el costo por plato y su precio de venta.

Desarrollada en **Python + Streamlit**, con la base de datos en **Supabase (PostgreSQL)**.


## Funcionalidades

### Perfil Cocina
- Seleccionar el menú e ingresar la cantidad de comensales. No se aceptan valores vacíos, negativos ni cero.
- Ver la **orden de preparación**: las unidades completas que se deben retirar (kg, paquetes, empaques) y la cantidad exacta que se usa en la preparación (por ejemplo, 37,5 papas).
- Cada orden se guarda automáticamente en la base de datos.
- Este perfil **no ve** costos, pérdidas ni precios.

### Perfil Administrador
- **Resumen:** total de servicios realizados, costo total de operación, pérdida total por merma e ingresos proyectados.
- **Historial:** tabla con todas las órdenes, filtrable por menú, más el desglose de cada orden por ingrediente.
- **Análisis de mermas:** gráficos de pérdida por menú y por ingrediente, para identificar dónde se pierde más dinero.
- **Nueva orden:** también puede generar órdenes de preparación.

---

## Cómo se calcula

Los productos **no se pueden dividir ni guardar** una vez abiertos. Por eso siempre se compran unidades completas, y lo que sobra se considera merma.

Cada receta indica la cantidad de cada ingrediente para **4 comensales**. Cada unidad de compra tiene un **contenido** expresado en la misma unidad de la receta. Por ejemplo, 1 kg de papas = 4 papas, y 1 paquete de arroz = 10 porciones.

| Concepto | Fórmula |
|---|---|
| Cantidad necesaria | `cantidad de la receta × comensales / 4` |
| Unidades a utilizar | `ceil(cantidad necesaria / contenido)` (redondeo hacia arriba) |
| Cantidad sobrante | `unidades × contenido − cantidad necesaria` |
| Merma física | `cantidad sobrante / contenido` (fracción de unidad no usada) |
| Costo del ingrediente | `unidades × costo unitario` |
| Pérdida por merma | `merma física × costo unitario` |
| Costo por plato | `costo total del menú / comensales` |
| Precio de venta por plato | `costo por plato × 1,25` (25 % de ganancia sobre el precio costo) |

**Ejemplo.** Tortilla de Papas y Cebolla para 25 comensales. La receta pide 6 papas por cada 4 comensales:
- Papas necesarias: 6 × 25 / 4 = 37,5 papas
- Como 1 kg = 4 papas, se usan ceil(37,5 / 4) = **10 kg** (40 papas)
- Sobran 2,5 papas = 0,625 kg, y la pérdida por merma es 0,625 × $1.000 = **$625**

### Supuestos
- Las cantidades de cada menú se obtienen escalando su receta (base 4 comensales) en forma proporcional a los comensales.
- Contenido de cada unidad de compra: 1 kg de papas = 4 papas, 1 kg de tomates = 4 tomates, 1 empaque = 12 huevos, y 1 paquete o litro trae tantas porciones como personas indica su rendimiento.
- La cebolla rinde para 4 personas por unidad.
- La merma se valoriza en forma proporcional al costo de la unidad.

---

## Catálogo

| Ingrediente | Costo | Unidad de compra | Contenido |
|---|---|---|---|
| Cebolla | $500 | unidad | 1 cebolla |
| Arroz | $1.500 | paquete | 10 porciones |
| Tuto de pollo | $1.200 | unidad | 1 tuto |
| Carne molida | $1.500 | paquete | 4 porciones |
| Papa | $1.000 | kg | 4 papas |
| Tomate | $1.500 | kg | 4 tomates |
| Fideos | $1.200 | paquete | 4 porciones |
| Lechuga | $1.000 | unidad | 1 lechuga |
| Huevo | $4.500 | empaque | 12 huevos |
| Aceite | $1.000 | litro | 10 porciones |

Menús disponibles: Arroz con Pollo y Ensalada · Carne Molida con Papas y Arroz · Tallarines con Salsa de Tomate · Tortilla de Papas y Cebolla · Pollo Salteado con Verduras · Charquicán Simple · Fideos con Huevo y Tomate · Carne Molida con Arroz y Ensalada · Papas Cocidas con Huevo y Lechuga · Arroz Graneado con Huevo y Cebolla.

---

## Estructura del proyecto

```
rancho_merma/
├── app.py                     Punto de entrada: inicio de sesión y navegación por rol
├── modulos/
│   ├── conexion.py            Conexión a Supabase usando st.secrets
│   ├── datos.py               Consultas e inserciones en la base de datos
│   ├── calculos.py            Motor de cálculo: cantidades, merma, costos y precio
│   ├── vista_cocina.py        Pantalla del perfil cocina
│   └── vista_admin.py         Panel del perfil administrador
├── sql/
│   ├── 01_esquema.sql         Tablas, vistas, roles, función de login y permisos
│   └── 02_datos.sql           Ingredientes, recetas y usuarios iniciales
├── pruebas/
│   └── prueba_calculos.py     Verificación del motor de cálculo
├── .streamlit/
│   └── secrets.toml.example   Plantilla de credenciales
└── requirements.txt
```

### Base de datos

| Tabla / vista | Contenido |
|---|---|
| `ingredientes` | Catálogo con costo, unidad de compra, rendimiento y contenido |
| `recetas` | Menús disponibles |
| `receta_ingredientes` | Ingredientes de cada menú y su cantidad para 4 comensales |
| `ordenes` | Cada servicio solicitado: menú, comensales, costos, pérdida e ingreso |
| `orden_detalle` | Insumos de cada orden: unidades, cantidad necesaria, sobrante, merma, costo y pérdida |
| `usuarios` | Usuarios con contraseña encriptada (bcrypt) y su rol |
| `v_ordenes`, `v_detalle` | Vistas de consulta para el panel del administrador |

---

## Instalación

### Requisitos
- Python 3.10 o superior
- Una cuenta en [Supabase](https://supabase.com)

### 1. Crear la base de datos
1. Crear un proyecto en Supabase.
2. En **SQL Editor**, ejecutar `sql/01_esquema.sql` y luego `sql/02_datos.sql`.
3. La consulta final debe mostrar **10 ingredientes, 10 recetas y 40 relaciones**.

### 2. Configurar las credenciales
1. En la carpeta `.streamlit`, copiar `secrets.toml.example` con el nombre `secrets.toml`.
2. Completar los datos con la información de **Project Settings → API Keys** del proyecto:
   ```toml
   SUPABASE_URL = "https://TU-PROYECTO.supabase.co"
   SUPABASE_KEY = "TU-LLAVE-ANON-O-PUBLISHABLE"
   ```
   Se debe usar la llave pública (anon/publishable), nunca la `service_role`.
   El archivo `secrets.toml` está excluido en `.gitignore`, para que las credenciales no queden publicadas.

### 3. Ejecutar
Desde la carpeta del proyecto, ejecutar en la terminal:
```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```
La aplicación se abre en el navegador, en `http://localhost:8501`.

Para verificar el motor de cálculo sin conexión a internet:
```bash
python -m pruebas.prueba_calculos
```

---

## Usuarios de prueba

| Usuario | Contraseña | Rol |
|---|---|---|
| `cocina` | `cocina123` | Cocina |
| `admin` | `admin123` | Administrador |

---

## Seguridad
- Las credenciales se leen desde `st.secrets` y no están escritas en el código.
- Las contraseñas se almacenan encriptadas con bcrypt.
- Row Level Security está activado en todas las tablas. La aplicación solo puede leer el catálogo y registrar o consultar órdenes.
- La tabla `usuarios` no es accesible desde la aplicación. El inicio de sesión se valida con la función `validar_usuario()`, que devuelve únicamente el rol.
