-- =====================================================================
-- ACTIVIDAD 1: Modelamiento de la Base de Datos en Supabase
-- Ejecutar en: Supabase > SQL Editor > New query > pegar todo > Run
-- Orden: primero este archivo (01_esquema.sql), luego 02_datos.sql
-- =====================================================================

-- Extensión para encriptar contraseñas (en Supabase ya viene instalada,
-- esta línea solo asegura que exista).
create extension if not exists pgcrypto with schema extensions;

-- ---------------------------------------------------------------------
-- 1) CATÁLOGO DE INGREDIENTES
--    rendimiento      = utilidad de la tabla del enunciado (personas por unidad)
--    contenido        = cuánto trae 1 unidad de compra, en la unidad de la
--                       receta. Se usa en el cálculo.
--                       Ej: 1 kg de papas = 4 papas; 1 paquete de arroz = 10 porciones
--    unidad_contenido = nombre de esa unidad (papas, porciones, huevos...)
-- ---------------------------------------------------------------------
create table if not exists ingredientes (
    id                serial primary key,
    nombre            text not null unique,
    costo_unitario    numeric(12,2) not null check (costo_unitario > 0),
    unidad_compra     text not null,          -- unidad, paquete, kg, litro, empaque
    rendimiento       integer not null check (rendimiento > 0),
    contenido         numeric(10,2) not null check (contenido > 0),
    unidad_contenido  text not null
);

-- ---------------------------------------------------------------------
-- 2) RECETAS (MENÚS)
-- ---------------------------------------------------------------------
create table if not exists recetas (
    id                serial primary key,
    nombre            text not null unique,
    comensales_base   integer not null default 4
);

-- Tabla intermedia receta <-> ingrediente (relación muchos a muchos).
-- cantidad_base y unidad_receta guardan lo indicado en la receta original
-- (base 4 comensales) para referencia.
create table if not exists receta_ingredientes (
    id              serial primary key,
    receta_id       integer not null references recetas(id) on delete cascade,
    ingrediente_id  integer not null references ingredientes(id),
    cantidad_base   numeric(10,2) not null,
    unidad_receta   text not null,
    unique (receta_id, ingrediente_id)
);

-- ---------------------------------------------------------------------
-- 3) ÓRDENES DE SERVICIO (cada vez que cocina solicita un menú)
-- ---------------------------------------------------------------------
create table if not exists ordenes (
    id                    serial primary key,
    fecha                 timestamptz not null default now(),
    receta_id             integer not null references recetas(id),
    comensales            integer not null check (comensales > 0),
    costo_total           numeric(12,2) not null,
    costo_por_plato       numeric(12,2) not null,
    precio_venta_plato    numeric(12,2) not null,
    ingreso_total         numeric(12,2) not null,
    perdida_merma_total   numeric(12,2) not null,
    usuario               text not null
);

-- Detalle de insumos calculados por cada orden
create table if not exists orden_detalle (
    id                    serial primary key,
    orden_id              integer not null references ordenes(id) on delete cascade,
    ingrediente_id        integer not null references ingredientes(id),
    unidades_compradas    integer not null,        -- unidades completas (math.ceil)
    cantidad_necesaria    numeric(10,2) not null,  -- lo que pide la receta escalada
    cantidad_sobrante     numeric(10,2) not null,  -- merma en unidades de la receta
    merma_fraccion        numeric(8,4) not null,   -- fracción de unidad no usada
    costo                 numeric(12,2) not null,  -- unidades * costo_unitario
    perdida_merma         numeric(12,2) not null   -- merma_fraccion * costo_unitario
);

-- ---------------------------------------------------------------------
-- 4) USUARIOS Y ROLES
--    La contraseña se guarda ENCRIPTADA (bcrypt), nunca en texto plano.
-- ---------------------------------------------------------------------
create table if not exists usuarios (
    id          serial primary key,
    usuario     text not null unique,
    clave_hash  text not null,
    rol         text not null check (rol in ('cocina', 'administrador'))
);

-- Función de login: recibe usuario y clave, devuelve el rol si son correctos.
-- "security definer" permite que la app valide SIN poder leer la tabla usuarios.
create or replace function validar_usuario(p_usuario text, p_clave text)
returns text
language sql
security definer
set search_path = public, extensions
as $$
    select rol
    from usuarios
    where usuario = p_usuario
      and clave_hash = extensions.crypt(p_clave, clave_hash);
$$;

-- ---------------------------------------------------------------------
-- 5) VISTAS para el panel del administrador (unen nombres con números)
-- ---------------------------------------------------------------------
create or replace view v_ordenes as
select o.id, o.fecha, r.nombre as menu, o.comensales, o.costo_total,
       o.costo_por_plato, o.precio_venta_plato, o.ingreso_total,
       o.perdida_merma_total, o.usuario
from ordenes o
join recetas r on r.id = o.receta_id;

create or replace view v_detalle as
select d.orden_id, r.nombre as menu, i.nombre as ingrediente, i.unidad_compra,
       d.unidades_compradas, d.cantidad_necesaria, i.unidad_contenido,
       d.cantidad_sobrante, d.merma_fraccion,
       d.costo, d.perdida_merma
from orden_detalle d
join ordenes o      on o.id = d.orden_id
join recetas r      on r.id = o.receta_id
join ingredientes i on i.id = d.ingrediente_id;

-- ---------------------------------------------------------------------
-- 6) SEGURIDAD (Row Level Security)
--    La app usa la llave pública (anon). Se habilita RLS y se permite
--    solo lo necesario. La tabla usuarios queda SIN políticas:
--    nadie la lee directamente, solo a través de validar_usuario().
-- ---------------------------------------------------------------------
alter table ingredientes        enable row level security;
alter table recetas             enable row level security;
alter table receta_ingredientes enable row level security;
alter table ordenes             enable row level security;
alter table orden_detalle       enable row level security;
alter table usuarios            enable row level security;

create policy "leer ingredientes" on ingredientes        for select to anon using (true);
create policy "leer recetas"      on recetas             for select to anon using (true);
create policy "leer receta_ing"   on receta_ingredientes for select to anon using (true);
create policy "leer ordenes"      on ordenes             for select to anon using (true);
create policy "crear ordenes"     on ordenes             for insert to anon with check (true);
create policy "leer detalle"      on orden_detalle       for select to anon using (true);
create policy "crear detalle"     on orden_detalle       for insert to anon with check (true);

-- Permisos de la llave pública (anon). Los proyectos nuevos de Supabase
-- ya no los entregan automáticamente, por eso se otorgan aquí.
-- Sobre usuarios NO se otorga nada: solo se usa validar_usuario().
grant usage on schema public to anon;
grant select on ingredientes, recetas, receta_ingredientes to anon;
grant select, insert on ordenes, orden_detalle to anon;
grant select on v_ordenes, v_detalle to anon;
grant usage on all sequences in schema public to anon;

grant execute on function validar_usuario(text, text) to anon;
