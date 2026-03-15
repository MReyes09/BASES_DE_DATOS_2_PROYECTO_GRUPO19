
***

## Niveles de Dependencia

| **Nivel** | **Descripción**                      | **Cantidad Tablas** | **Total Acumulado** |
|-----------|--------------------------------------|---------------------|---------------------|
| **1**     | Tablas SIN FK (independientes)      | 7 tablas            | 7                   |
| **2**     | Tablas con 1 FK                     | 4 tablas            | 11                  |
| **3**     | Tablas con 2 o más FK               | 11 tablas           | 22                  |
| **4**     | No aplica (todas cubiertas)         | 0                   | **22**              |

***

## Nivel 1 - Tablas Independientes (7 tablas)

| **Orden** | **Tabla**       | **Motivo**                      |
|-----------|-----------------|---------------------------------|
| 1         | `Fase`          | Catálogo de fases               |
| 2         | `Grupo`         | Catálogo de grupos (A, B, C…)   |
| 3         | `Jugador`       | Datos base de jugadores         |
| 4         | `Mundial`       | Información de mundiales        |
| 5         | `Pais`          | Países participantes            |
| 6         | `Tipo_Premio`   | Tipos de premios                |
| 7         | `Tipo_Tarjeta`  | Amarilla/Roja                   |

***

## Nivel 2 - Tablas con 1 Dependencia (4 tablas)

| **Orden** | **Tabla**         | **Depende de** |
|-----------|-------------------|----------------|
| 8         | `Premio`          | `Mundial`      |
| 9         | `Red_social`      | `Jugador`      |
| 10        | `Plantilla`       | `Pais`         |
| 11        | `Llave_Mundial`   | `Mundial`      |

> Nota: `Llave_Fase_Mundial` usa `Llave_Mundial` y `Fase`, por eso va después (nivel 3).

***

## Nivel 3 - Tablas con 2 o más Dependencias (11 tablas)

| **Orden** | **Tabla**                 | **Depende de**                                   |
|-----------|--------------------------|--------------------------------------------------|
| 12        | `Llave_Fase_Mundial`     | `Llave_Mundial`, `Fase`                          |
| 13        | `Evento_Partido`         | `Llave_Mundial`                                  |
| 14        | `Evento_Cambio_Jugador`  | `Evento_Partido`                                 |
| 15        | `Pais_Clasificado_Mundial` | `Mundial`, `Pais`, `Grupo`                    |
| 16        | `Evento_Falta`           | `Evento_Partido`, `Tipo_Tarjeta`                |
| 17        | `Evento_Gol`             | `Evento_Partido`, `Jugador`                     |
| 18        | `Partido_Plantilla`      | `Plantilla`, `Evento_Partido`                   |
| 19        | `Posicion_Jugador`       | `Plantilla`, `Jugador`                          |
| 20        | `Premio_Tipo_Premio`     | `Premio`, `Tipo_Premio`                         |
| 21        | `Premios_Jugador`        | `Premio`, `Jugador`                             |
| 22        | `Cambio_Jugador`         | `Evento_Cambio_Jugador`, `Jugador`              |

***

## Secuencia Completa de Inserción (resumen)

```sql
-- NIVEL 1: Tablas sin FK
INSERT INTO Fase (...);
INSERT INTO Grupo (...);
INSERT INTO Jugador (...);
INSERT INTO Mundial (...);
INSERT INTO Pais (...);
INSERT INTO Tipo_Premio (...);
INSERT INTO Tipo_Tarjeta (...);

-- NIVEL 2: Tablas con 1 FK
INSERT INTO Premio (...);          -- FK Mundial_id_mu
INSERT INTO Red_social (...);      -- FK Jugador_id_ju
INSERT INTO Plantilla (...);       -- FK Pais_id_pa
INSERT INTO Llave_Mundial (...);   -- FK Mundial_id_mu

-- NIVEL 3: Tablas con 2+ FKs
INSERT INTO Llave_Fase_Mundial (...);        -- Llave_Mundial, Fase
INSERT INTO Evento_Partido (...);            -- Llave_Mundial
INSERT INTO Evento_Cambio_Jugador (...);     -- Evento_Partido
INSERT INTO Pais_Clasificado_Mundial (...);  -- Mundial, Pais, Grupo
INSERT INTO Evento_Falta (...);              -- Evento_Partido, Tipo_Tarjeta
INSERT INTO Evento_Gol (...);                -- Evento_Partido, Jugador
INSERT INTO Partido_Plantilla (...);         -- Plantilla, Evento_Partido
INSERT INTO Posicion_Jugador (...);          -- Plantilla, Jugador
INSERT INTO Premio_Tipo_Premio (...);        -- Premio, Tipo_Premio
INSERT INTO Premios_Jugador (...);           -- Premio, Jugador
INSERT INTO Cambio_Jugador (...);            -- Evento_Cambio_Jugador, Jugador
```
