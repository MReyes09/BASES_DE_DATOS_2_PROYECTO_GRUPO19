# Niveles de Dependencia **(ACTUALIZADO)**

## Niveles de Dependencia

| **Nivel** | **Descripción** | **Cantidad Tablas** | **Estado** | **Total Acumulado** |
|-----------|-----------------|---------------------|------------|---------------------|
| **1** | Tablas SIN FK (independientes) | 7 tablas | ✅ **COMPLETO** | 7 |
| **2** | Tablas con 1 FK | 4 tablas | ✅ **COMPLETO** | 11 |
| **3** | Tablas con 2 o más FK | 11 tablas | 🔴 **0/11 (0%)** | **22** |

## Nivel 1 - Tablas Independientes **(✅ YA CARGADO)**

| **Orden** | **Tabla** | **Motivo** |
|-----------|-----------|------------|
| 1 | `Fase` | Catálogo de fases |
| 2 | `Grupo` | Catálogo de grupos (A, B, C…) |
| 3 | `Jugador` | Datos base de jugadores |
| 4 | `Mundial` | Información de mundiales |
| 5 | `Pais` | Países participantes |
| 6 | `Tipo_Premio` | Tipos de premios **(NUEVO: 1:1 con Premio)** |
| 7 | `Tipo_Tarjeta` | Amarilla/Roja |

## Nivel 2 - Tablas con 1 Dependencia **(✅ YA CARGADO)**

| **Orden** | **Tabla** | **Depende de** | **Estado** |
|-----------|-----------|----------------|------------|
| 8 | `Premio` | `Mundial` | 🟡 PARCIAL |
| 9 | `Red_social` | `Jugador` | ✅ **CARGADO** |
| 10 | `Plantilla` | `Pais` | ✅ **CARGADO** |
| 11 | `Llave_Mundial` | `Mundial` | ✅ **CARGADO** |

## Nivel 3 - Tablas con 2 o más Dependencias **(🟡 PARCIAL)**

| **Orden** | **Tabla** | **Depende de** | **Estado** |
|-----------|-----------|----------------|------------|
| 12 | `Evento_Partido` | `Llave_Mundial` | ✅ **CARGADO** |
| 13 | `Evento_Cambio_Jugador` | `Evento_Partido` | ✅ **CARGADO** |
| 14 | `Pais_Clasificado_Mundial` | `Mundial`, `Pais`, `Grupo` | 🔴 **PENDIENTE** |
| 15 | `Evento_Falta` | `Evento_Partido`, `Tipo_Tarjeta` | 🟡 PARCIAL |
| 16 | `Evento_Gol` | `Evento_Partido`, `Jugador` | ✅ **CARGADO** |
| 17 | `Partido_Plantilla` | `Plantilla`, `Evento_Partido` | ✅ **CARGADO** |
| 18 | `Posicion_Jugador` | `Plantilla`, `Jugador` | 🔴 **PENDIENTE** |
| 19 | `Premios_Jugador` | `Premio`, `Jugador` | 🟡 PARCIAL |
| 20 | `Cambio_Jugador` | `Evento_Cambio_Jugador`, `Jugador` | ✅ **CARGADO** |

## Secuencia Completa de Inserción **(ACTUALIZADA)**

```sql
-- ✅ NIVEL 1: COMPLETO (7/7)
-- Fase ✓, Grupo ✓, Jugador ✓, Mundial ✓, Pais ✓, Tipo_Premio ✓, Tipo_Tarjeta ✓

-- 🟡 NIVEL 2: PARCIAL (1/4) - SIGUIENTES 3 INSERTS 👇
INSERT INTO Premio (...);           -- FK Mundial_id_mu ✓ + Tipo_Premio_id_ti_pre ✓
INSERT INTO Plantilla (...);        -- FK Pais_id_pa ✓
INSERT INTO Llave_Mundial (...);    -- FK Mundial_id_mu ✓

-- 🔴 NIVEL 3: SIN INICIAR (0/11)
INSERT INTO Llave_Fase_Mundial (...);     -- Llave_Mundial, Fase ✓
INSERT INTO Evento_Partido (...);         -- Llave_Mundial
INSERT INTO Evento_Cambio_Jugador (...);  -- Evento_Partido
INSERT INTO Pais_Clasificado_Mundial (...); -- Mundial ✓, Pais ✓, Grupo ✓
INSERT INTO Evento_Falta (...);           -- Evento_Partido, Tipo_Tarjeta ✓
INSERT INTO Evento_Gol (...);             -- Evento_Partido, Jugador ✓
INSERT INTO Partido_Plantilla (...);      -- Plantilla, Evento_Partido
INSERT INTO Posicion_Jugador (...);       -- Plantilla, Jugador ✓
INSERT INTO Premios_Jugador (...);        -- Premio, Jugador ✓
INSERT INTO Cambio_Jugador (...);         -- Evento_Cambio_Jugador, Jugador ✓
```
