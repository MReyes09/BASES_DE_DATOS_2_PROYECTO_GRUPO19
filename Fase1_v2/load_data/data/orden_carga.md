Aquí va igual que tu documentación original, pero actualizado al modelo sin EQUIPO.

## Niveles de Dependencia

| **Nivel** | **Descripción**                          | **Cantidad Tablas** | **Total Acumulado** |
|-----------|-------------------------------------------|---------------------|---------------------|
| **1**     | Tablas SIN FK (independientes)           | 6 tablas            | 6                   |
| **2**     | Tablas con 1 FK                          | 5 tablas            | 11                  |
| **3**     | Tablas con 2 o más FK                    | 10 tablas           | 21                  |
| **4**     | No aplica (todas cubiertas)              | 0                   | **21**              |

***

## Nivel 1 - Tablas Independientes (6 tablas)

| **Orden** | **Tabla**       | **Motivo**                 |
|-----------|-----------------|----------------------------|
| 1         | `Fase`          | Catálogo de fases          |
| 2         | `Jugador`       | Datos base de jugadores    |
| 3         | `Mundial`       | Información de mundiales   |
| 4         | `Pais`          | Países participantes       |
| 5         | `Tipo_Premio`   | Tipos de premios           |
| 6         | `Tipo_Tarjeta`  | Amarilla/Roja              |

***

## Nivel 2 - Tablas con 1 Dependencia (5 tablas)

| **Orden** | **Tabla**       | **Depende de** |
|-----------|-----------------|----------------|
| 7         | `Grupo`         | `Mundial`      |
| 8         | `Premio`        | `Mundial`      |
| 9         | `Red_social`    | `Jugador`      |
| 10        | `Plantilla`     | `Pais`         |
| 11        | `Llave_Mundial` | `Mundial`, `Fase` (ambas ya nivel 1) |

***

## Nivel 3 - Tablas con 2 o más Dependencias (10 tablas)

| **Orden** | **Tabla**                | **Depende de**                          |
|-----------|--------------------------|-----------------------------------------|
| 12        | `Evento_Partido`         | `Llave_Mundial`                         |
| 13        | `Evento_Cambio_Jugador` | `Evento_Partido`                        |
| 14        | `Pais_Clasificado`      | `Pais`, `Grupo`                         |
| 15        | `Evento_Falta`          | `Evento_Partido`, `Tipo_Tarjeta`       |
| 16        | `Evento_Gol`            | `Evento_Partido`, `Jugador`            |
| 17        | `Partido_Plantilla`     | `Plantilla`, `Evento_Partido`          |
| 18        | `Posicion_Jugador`      | `Plantilla`, `Jugador`                 |
| 19        | `Premio_Tipo_Premio`    | `Premio`, `Tipo_Premio`                |
| 20        | `Premios_Jugador`       | `Premio`, `Jugador`                    |
| 21        | `Cambio_Jugador`        | `Evento_Cambio_Jugador`, `Jugador`     |

***

## Secuencia Completa de Inserción (resumen)

```sql
-- NIVEL 1
INSERT INTO Fase (...);
INSERT INTO Jugador (...);
INSERT INTO Mundial (...);
INSERT INTO Pais (...);
INSERT INTO Tipo_Premio (...);
INSERT INTO Tipo_Tarjeta (...);

-- NIVEL 2
INSERT INTO Grupo (...);
INSERT INTO Premio (...);
INSERT INTO Red_social (...);
INSERT INTO Plantilla (...);
INSERT INTO Llave_Mundial (...);

-- NIVEL 3
INSERT INTO Evento_Partido (...);
INSERT INTO Evento_Cambio_Jugador (...);
INSERT INTO Pais_Clasificado (...);
INSERT INTO Evento_Falta (...);
INSERT INTO Evento_Gol (...);
INSERT INTO Partido_Plantilla (...);
INSERT INTO Posicion_Jugador (...);
INSERT INTO Premio_Tipo_Premio (...);
INSERT INTO Premios_Jugador (...);
INSERT INTO Cambio_Jugador (...);
```