# Documentación: Orden de Inserción DDL Mundial de Fútbol (V3 Actualizado)

El orden correcto para insertar datos en tu base de datos sigue los niveles de dependencia de las claves foráneas, evitando errores de violación de FK. Hay 22 tablas en total, organizadas en 4 niveles según el número de tablas padre requeridas.

## Niveles de Dependencia

| **Nivel** | **Descripción** | **Cantidad Tablas** | **Total Acumulado** |
|-----------|-----------------|--------------------|---------------------|
| **1** | Tablas SIN FK (independientes) | 6 tablas | 6 |
| **2** | Tablas con 1 FK | 7 tablas | 13 |
| **3** | Tablas con 2 FK | 9 tablas | 22 |
| **4** | No aplica (todas cubiertas) | 0 | **22**  |

## Nivel 1 - Tablas Independientes (6 tablas)

Estas tablas no dependen de ninguna otra y se insertan primero.

| **Orden** | **Tabla** | **Motivo** |
|-----------|-----------|------------|
| 1 | `Fase` | Catálogo de fases |
| 2 | `Jugador` | Datos base de jugadores |
| 3 | `Mundial` | Información de mundiales |
| 4 | `Pais` | Países participantes |
| 5 | `Tipo_Premio` | Tipos de premios |
| 6 | `Tipo_Tarjeta` | Amarilla/Roja  |

**Comando:** `INSERT INTO` estas tablas en cualquier orden interno.

## Nivel 2 - Tablas con 1 Dependencia (7 tablas)

Dependencias directas del Nivel 1.

| **Orden** | **Tabla** | **Depende de** |
|-----------|-----------|----------------|
| 7 | `Equipo` | `Pais` |
| 8 | `Grupo` | `Mundial` |
| 9 | `Premio` | `Mundial` |
| 10 | `Red_social` | `Jugador` |
| 11 | `Plantilla` | `Equipo` |
| 12 | `Evento_Partido` | `Llave_Mundial` (ver Nivel 3 primero) |
| 13 | `Evento_Cambio_Jugador` | `Evento_Partido`  |

**Nota:** `Llave_Mundial` (2 deps) se necesita aquí; insertar después.

## Nivel 3 - Tablas con 2 Dependencias (9 tablas)

Requieren Niveles 1 y 2 completos.

| **Orden** | **Tabla** | **Depende de** |
|-----------|-----------|----------------|
| 14 | `Llave_Mundial` | `Mundial`, `Fase` |
| 15 | `Pais_Clasificado` | `Pais`, `Grupo` |
| 16 | `Evento_Falta` | `Evento_Partido`, `Tipo_Tarjeta` |
| 17 | `Evento_Gol` | `Evento_Partido`, `Jugador` |
| 18 | `Partido_Plantilla` | `Plantilla`, `Evento_Partido` |
| 19 | `Posicion_Jugador` | `Plantilla`, `Jugador` |
| 20 | `Premio_Tipo_Premio` | `Premio`, `Tipo_Premio` |
| 21 | `Premios_Jugador` | `Premio`, `Jugador` |
| 22 | `Cambio_Jugador` | `Evento_Cambio_Jugador`, `Jugador`  |

## Secuencia Completa de Inserción

```sql
-- 🎯 NIVEL 1: Independientes (6 tablas)
INSERT INTO Fase VALUES (...);
INSERT INTO Jugador VALUES (...);
INSERT INTO Mundial VALUES (...);
INSERT INTO Pais VALUES (...);
INSERT INTO Tipo_Premio VALUES (...);
INSERT INTO Tipo_Tarjeta VALUES (...);

-- 🎯 NIVEL 2: 1 dependencia (7 tablas)
INSERT INTO Equipo VALUES (...);
INSERT INTO Grupo VALUES (...);
INSERT INTO Premio VALUES (...);
INSERT INTO Red_social VALUES (...);
INSERT INTO Plantilla VALUES (...);
INSERT INTO Llave_Mundial VALUES (...);  -- Requiere Nivel 1
INSERT INTO Evento_Partido VALUES (...);
INSERT INTO Evento_Cambio_Jugador VALUES (...);

-- 🎯 NIVEL 3: 2 dependencias (9 tablas)
INSERT INTO Pais_Clasificado VALUES (...);
INSERT INTO Evento_Falta VALUES (...);
INSERT INTO Evento_Gol VALUES (...);
INSERT INTO Partido_Plantilla VALUES (...);
INSERT INTO Posicion_Jugador VALUES (...);
INSERT INTO Premio_Tipo_Premio VALUES (...);
INSERT INTO Premios_Jugador VALUES (...);
INSERT INTO Cambio_Jugador VALUES (...); [code_file:1]
```

Este orden garantiza que todas las claves foráneas existan antes de insertar. Usa las secuencias proporcionadas para generar IDs autoincrementales.