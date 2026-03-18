# Niveles de Dependencia **(ACTUALIZADO)**

## Niveles de Dependencia

| **Nivel** | **Descripción** | **Cantidad Tablas** | **Estado** | **Total Acumulado** |
|-----------|-----------------|---------------------|------------|---------------------|
| **1** | Tablas SIN FK (independientes) | 7 tablas | ✅ **COMPLETO** | 7 |
| **2** | Tablas con 1 FK | 4 tablas | ✅ **COMPLETO** | 11 |
| **3** | Tablas con 2 o más FK | 11 tablas |  🟡 **9/11 (81.82%)** | **22** |

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
| 8 | `Premio` | `Mundial` | ✅ **CARGADO** |
| 9 | `Red_social` | `Jugador` | ✅ **CARGADO** |
| 10 | `Plantilla` | `Pais` | ✅ **CARGADO** |
| 11 | `Llave_Mundial` | `Mundial` | ✅ **CARGADO** |

## Nivel 3 - Tablas con 2 o más Dependencias **(🟡 PARCIAL)**

| **Orden** | **Tabla** | **Depende de** | **Estado** |
|-----------|-----------|----------------|------------|
| 12 | `Evento_Partido` | `Llave_Mundial` | ✅ **CARGADO** |
| 13 | `Evento_Cambio_Jugador` | `Evento_Partido` | ✅ **CARGADO** |
| 14 | `Pais_Clasificado_Mundial` | `Mundial`, `Pais`, `Grupo` | ✅ **CARGADO** |
| 15 | `Evento_Falta` | `Evento_Partido`, `Tipo_Tarjeta` | ✅ **CARGADO** |
| 16 | `Evento_Gol` | `Evento_Partido`, `Jugador` | ✅ **CARGADO** |
| 17 | `Partido_Plantilla` | `Plantilla`, `Evento_Partido` | ✅ **CARGADO** |
| 18 | `Posicion_Jugador` | `Plantilla`, `Jugador` | 🔴 **PENDIENTE** |
| 19 | `Premios_Jugador` | `Premio`, `Jugador` | ✅ **CARGADO** |
| 20 | `Cambio_Jugador` | `Evento_Cambio_Jugador`, `Jugador` | ✅ **CARGADO** |
