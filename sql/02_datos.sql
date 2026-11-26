-- =====================================================================
-- ACTIVIDAD 1: Población inicial del catálogo (10 ingredientes + 10 recetas)
-- Ejecutar DESPUÉS de 01_esquema.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- Ingredientes (tabla del enunciado + correcciones)
-- rendimiento = utilidad de la tabla (personas por unidad de compra)
-- contenido   = cuánto trae 1 unidad de compra en la unidad de la receta
--   Correcciones: cebolla = 4 personas; 1 kg = 4 papas; 1 kg = 4 tomates
-- ---------------------------------------------------------------------
insert into ingredientes (nombre, costo_unitario, unidad_compra, rendimiento, contenido, unidad_contenido) values
    ('Cebolla',       500,  'unidad',  4,  1,  'cebollas'),
    ('Arroz',         1500, 'paquete', 10, 10, 'porciones'),
    ('Tuto de pollo', 1200, 'unidad',  1,  1,  'tutos'),
    ('Carne molida',  1500, 'paquete', 4,  4,  'porciones'),
    ('Papa',          1000, 'kg',      4,  4,  'papas'),
    ('Tomate',        1500, 'kg',      6,  4,  'tomates'),
    ('Fideos',        1200, 'paquete', 4,  4,  'porciones'),
    ('Lechuga',       1000, 'unidad',  10, 1,  'lechugas'),
    ('Huevo',         4500, 'empaque', 12, 12, 'huevos'),
    ('Aceite',        1000, 'litro',   10, 10, 'porciones');

-- ---------------------------------------------------------------------
-- Recetas (todas con base 4 comensales)
-- ---------------------------------------------------------------------
insert into recetas (nombre, comensales_base) values
    ('Arroz con Pollo y Ensalada', 4),
    ('Carne Molida con Papas y Arroz', 4),
    ('Tallarines con Salsa de Tomate', 4),
    ('Tortilla de Papas y Cebolla', 4),
    ('Pollo Salteado con Verduras', 4),
    ('Charquicán Simple', 4),
    ('Fideos con Huevo y Tomate', 4),
    ('Carne Molida con Arroz y Ensalada', 4),
    ('Papas Cocidas con Huevo y Lechuga', 4),
    ('Arroz Graneado con Huevo y Cebolla', 4);

-- ---------------------------------------------------------------------
-- Ingredientes de cada receta (se buscan los id por nombre)
-- ---------------------------------------------------------------------
insert into receta_ingredientes (receta_id, ingrediente_id, cantidad_base, unidad_receta)
select r.id, i.id, x.cantidad, x.unidad
from (values
    ('Arroz con Pollo y Ensalada',         'Tuto de pollo', 4, 'unidades'),
    ('Arroz con Pollo y Ensalada',         'Arroz',         4, 'porciones'),
    ('Arroz con Pollo y Ensalada',         'Lechuga',       1, 'unidad'),
    ('Arroz con Pollo y Ensalada',         'Aceite',        4, 'porciones'),

    ('Carne Molida con Papas y Arroz',     'Carne molida',  4, 'porciones'),
    ('Carne Molida con Papas y Arroz',     'Papa',          6, 'unidades'),
    ('Carne Molida con Papas y Arroz',     'Cebolla',       1, 'unidad'),
    ('Carne Molida con Papas y Arroz',     'Aceite',        4, 'porciones'),

    ('Tallarines con Salsa de Tomate',     'Fideos',        4, 'porciones'),
    ('Tallarines con Salsa de Tomate',     'Tomate',        4, 'unidades'),
    ('Tallarines con Salsa de Tomate',     'Cebolla',       1, 'unidad'),
    ('Tallarines con Salsa de Tomate',     'Aceite',        4, 'porciones'),

    ('Tortilla de Papas y Cebolla',        'Papa',          6, 'unidades'),
    ('Tortilla de Papas y Cebolla',        'Cebolla',       1, 'unidad'),
    ('Tortilla de Papas y Cebolla',        'Huevo',         6, 'unidades'),
    ('Tortilla de Papas y Cebolla',        'Aceite',        4, 'porciones'),

    ('Pollo Salteado con Verduras',        'Tuto de pollo', 4, 'unidades'),
    ('Pollo Salteado con Verduras',        'Tomate',        3, 'unidades'),
    ('Pollo Salteado con Verduras',        'Cebolla',       1, 'unidad'),
    ('Pollo Salteado con Verduras',        'Aceite',        4, 'porciones'),

    ('Charquicán Simple',                  'Papa',          6, 'unidades'),
    ('Charquicán Simple',                  'Lechuga',       1, 'unidad'),
    ('Charquicán Simple',                  'Cebolla',       1, 'unidad'),
    ('Charquicán Simple',                  'Aceite',        4, 'porciones'),

    ('Fideos con Huevo y Tomate',          'Fideos',        4, 'porciones'),
    ('Fideos con Huevo y Tomate',          'Huevo',         4, 'unidades'),
    ('Fideos con Huevo y Tomate',          'Tomate',        3, 'unidades'),
    ('Fideos con Huevo y Tomate',          'Aceite',        4, 'porciones'),

    ('Carne Molida con Arroz y Ensalada',  'Carne molida',  4, 'porciones'),
    ('Carne Molida con Arroz y Ensalada',  'Arroz',         4, 'porciones'),
    ('Carne Molida con Arroz y Ensalada',  'Lechuga',       1, 'unidad'),
    ('Carne Molida con Arroz y Ensalada',  'Tomate',        2, 'unidades'),

    ('Papas Cocidas con Huevo y Lechuga',  'Papa',          6, 'unidades'),
    ('Papas Cocidas con Huevo y Lechuga',  'Huevo',         4, 'unidades'),
    ('Papas Cocidas con Huevo y Lechuga',  'Lechuga',       1, 'unidad'),
    ('Papas Cocidas con Huevo y Lechuga',  'Aceite',        4, 'porciones'),

    ('Arroz Graneado con Huevo y Cebolla', 'Arroz',         4, 'porciones'),
    ('Arroz Graneado con Huevo y Cebolla', 'Huevo',         4, 'unidades'),
    ('Arroz Graneado con Huevo y Cebolla', 'Cebolla',       1, 'unidad'),
    ('Arroz Graneado con Huevo y Cebolla', 'Aceite',        4, 'porciones')
) as x(receta, ingrediente, cantidad, unidad)
join recetas r      on r.nombre = x.receta
join ingredientes i on i.nombre = x.ingrediente;

-- ---------------------------------------------------------------------
-- Usuarios de prueba (contraseña encriptada con bcrypt)
--   cocina / cocina123          -> rol cocina
--   admin  / admin123           -> rol administrador
-- (Cámbialas si quieres; recuerda decirle al profesor cuáles son.)
-- ---------------------------------------------------------------------
insert into usuarios (usuario, clave_hash, rol) values
    ('cocina', extensions.crypt('cocina123', extensions.gen_salt('bf')), 'cocina'),
    ('admin',  extensions.crypt('admin123',  extensions.gen_salt('bf')), 'administrador');

-- Verificación rápida (debe dar 10, 10 y 40)
select (select count(*) from ingredientes)        as ingredientes,
       (select count(*) from recetas)             as recetas,
       (select count(*) from receta_ingredientes) as receta_ingredientes;
