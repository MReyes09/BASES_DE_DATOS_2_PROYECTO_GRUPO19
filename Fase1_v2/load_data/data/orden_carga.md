
<div align="center">

**UNIVERSIDAD SAN CARLOS DE GUATEMALA**  
**FACULTAD DE INGENIERÍA**  
**LABORATORIO DE BASES DE DATOS 2**  
**SECCIÓN "N"**

**Documentación: Orden de Inserción DDL Mundial de Fútbol (V2 Actualizado)**

**Estudiantes:**  
**Daniel Andreé Hernandez Flores** - **202300512**  
**Matthew Emmanuel Reyes Melgar** - **202202233**  
**Dilan Conaher Suy Miranda** - **201801194**

**Guatemala — Marzo 2026**

</div>

---

## Índice

- [Índice](#índice)
- [Niveles de Dependencia](#niveles-de-dependencia)
- [Nivel 1 - Tablas Independientes (6 tablas)](#nivel-1---tablas-independientes-6-tablas)
- [Nivel 2 - Tablas con 1 Dependencia (7 tablas)](#nivel-2---tablas-con-1-dependencia-7-tablas)
- [Nivel 3 - Tablas con 2 Dependencias (5 tablas)](#nivel-3---tablas-con-2-dependencias-5-tablas)
- [Nivel 4 - Tablas con Múltiples Dependencias (3 tablas)](#nivel-4---tablas-con-múltiples-dependencias-3-tablas)
- [Secuencia Completa de Inserción](#secuencia-completa-de-inserción)

---

## Niveles de Dependencia

| **Nivel** | **Descripción** | **Cantidad Tablas** | **Total Acumulado** |
|-----------|-----------------|--------------------|-------------------|
| **1** | Tablas SIN FK (pueden insertarse primero) | 6 tablas | 6 |
| **2** | Tablas con 1 FK (dependen de Nivel 1) | 7 tablas | 13 |
| **3** | Tablas con 2 FK (dependen de Niveles 1-2) | 5 tablas | 18 |
| **4** | Tablas con ≥3 FK (dependen de todos) | 3 tablas | **21** |

---

## Nivel 1 - Tablas Independientes (6 tablas)

**Estas tablas NO tienen claves foráneas entrantes:**

| **Orden** | **Tabla** | **Motivo** |
|-----------|-----------|------------|
| 1 | `Pais` | Tabla base de países |
| 2 | `Fase` | Catálogo de fases del torneo |
| 3 | `Mundial` | Información de cada mundial |
| 4 | `Jugador` | Datos de jugadores |
| 5 | `Tipo_Tarjeta` | Amarilla/Roja |
| 6 | `Tipo_Premio` | Balón de Oro, Bota de Oro, etc. *(Nota: depende de Premio pero se inserta primero)* |

**`INSERT INTO` estas tablas primero**

---

## Nivel 2 - Tablas con 1 Dependencia (7 tablas)

**Dependencia directa de Nivel 1:**

| **Orden** | **Tabla** | **Depende de** |
|-----------|-----------|----------------|
| 7 | `Equipo` | `Pais` |
| 8 | `Grupo` | `Mundial` |
| 9 | `Llave_Mundial` | `Mundial`, `Fase` |
| 10 | `Pais_Clasificado` | `Pais`, `Grupo` |
| 11 | `Red_social` | `Jugador` |
| 12 | `Premio` | `Mundial` |
| 13 | `Evento_Partido` | `Llave_Mundial` |

**`INSERT INTO` después del Nivel 1 completo**

---

## Nivel 3 - Tablas con 2 Dependencias (5 tablas)

**Requieren Nivel 1 + Nivel 2:**

| **Orden** | **Tabla** | **Depende de** |
|-----------|-----------|----------------|
| 14 | `Plantilla` | `Equipo(id_eq, Pais_id_pa)` |
| 15 | `Evento_Gol` | `Evento_Partido`, `Jugador` |
| 16 | `Evento_Falta` | `Evento_Partido`, `Tipo_Tarjeta` |
| 17 | `Evento_Cambio_Jugador` | `Evento_Partido` |
| 18 | `Tipo_Premio` | `Premio` *(ahora sí)* |

**`INSERT INTO` después de completar Nivel 1 y 2**

---

## Nivel 4 - Tablas con Múltiples Dependencias (3 tablas)

**Requieren TODOS los niveles previos:**

| **Orden** | **Tabla** | **Depende de** |
|-----------|-----------|----------------|
| 19 | `Posicion_Jugador` | `Plantilla`, `Jugador` |
| 20 | `Partido_Plantilla` | `Plantilla`, `Evento_Partido` |
| 21 | `Cambio_Jugador` | `Evento_Cambio_Jugador`, `Jugador` |
| 22 | `Premios_Jugador` | `Premio`, `Jugador` |

**`INSERT INTO` DESPUÉS de completar los 3 niveles anteriores**

---

## Secuencia Completa de Inserción

```sql
-- 🎯 NIVEL 1: Tablas base (SIN FK) - 6 tablas
INSERT INTO Pais VALUES (...);
INSERT INTO Fase VALUES (...);
INSERT INTO Mundial VALUES (...);
INSERT INTO Jugador VALUES (...);
INSERT INTO Tipo_Tarjeta VALUES (...);
INSERT INTO Tipo_Premio VALUES (...);  -- Orden 6

-- 🎯 NIVEL 2: 1 dependencia - 7 tablas  
INSERT INTO Equipo VALUES (...);
INSERT INTO Grupo VALUES (...);
INSERT INTO Llave_Mundial VALUES (...);
INSERT INTO Pais_Clasificado VALUES (...);
INSERT INTO Red_social VALUES (...);
INSERT INTO Premio VALUES (...);
INSERT INTO Evento_Partido VALUES (...);  -- Orden 13

-- 🎯 NIVEL 3: 2 dependencias - 5 tablas
INSERT INTO Plantilla VALUES (...);
INSERT INTO Evento_Gol VALUES (...);
INSERT INTO Evento_Falta VALUES (...);
INSERT INTO Evento_Cambio_Jugador VALUES (...);
INSERT INTO Tipo_Premio VALUES (...);  -- Orden 18 (segunda pasada)

-- 🎯 NIVEL 4: Múltiples dependencias - 4 tablas
INSERT INTO Posicion_Jugador VALUES (...);
INSERT INTO Partido_Plantilla VALUES (...);
INSERT INTO Cambio_Jugador VALUES (...);
INSERT INTO Premios_Jugador VALUES (...);
```
