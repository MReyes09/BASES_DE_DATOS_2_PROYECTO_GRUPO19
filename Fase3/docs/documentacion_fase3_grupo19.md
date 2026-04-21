# Documentación Fase 3 - Grupo 19

## Integrantes

| Nombre Completo | Carnet |
|-----------------|--------|
| Daniel Andreé Hernandez Flores | 202300512 |
| Matthew Emmanuel Reyes Melgar | 202202233 |
| Dilan Conaher Suy Miranda | 201801194 |

---

## Índice

1. [Descripción General](#descripción-general)
2. [Tecnologías Utilizadas](#tecnologías-utilizadas)
3. [Arquitectura de la Base de Datos](#arquitectura-de-la-base-de-datos)
4. [Diseño del Modelo Documental](#diseño-del-modelo-documental)
5. [Configuración del Entorno con Docker](#configuración-del-entorno-con-docker)
6. [Script de Extracción: `parse_inserts.py`](#script-de-extracción-parse_insertspy)
7. [Script de Transformación: `build_mongo_collections.py`](#script-de-transformación-build_mongo_collectionspy)
8. [Carga de Datos con `mongoimport`](#carga-de-datos-con-mongoimport)
9. [Creación de Índices: `setup_indices.js`](#creación-de-índices-setup_indicesjs)
10. [Métodos de Consulta](#métodos-de-consulta)
    - [Método 1: Consulta por Año del Mundial](#método-1-consulta-por-año-del-mundial-getinfomundialjs)
    - [Método 2: Consulta por País](#método-2-consulta-por-país-gethistorialpaisjs)
11. [Estructura de Archivos del Proyecto](#estructura-de-archivos-del-proyecto)
12. [Orden de Ejecución](#orden-de-ejecución)

---

## Descripción General

Esta fase del proyecto consiste en migrar la base de datos relacional de Mundiales de Fútbol, originalmente construida en **Oracle SQL**, a una base de datos NoSQL utilizando **MongoDB**. El proceso abarca el rediseño del modelo de datos, la extracción y transformación de la información existente, y la construcción de métodos de consulta optimizados para las dos búsquedas requeridas: **por año del mundial** y **por país participante**.

La migración no consiste en trasladar las 20 tablas relacionales una por una hacia colecciones equivalentes, sino en **rediseñar el modelo** pensando en documentos, embebiendo la información relacionada para que cada consulta pueda resolverse de forma eficiente sin necesidad de múltiples joins.

---

## Tecnologías Utilizadas

| Tecnología | Versión / Detalle | Uso |
|---|---|---|
| MongoDB | Latest (imagen oficial Docker) | Motor de base de datos NoSQL |
| Docker Desktop | Windows | Contenedor del servidor MongoDB |
| MongoDB Compass | Última versión estable | Interfaz visual para explorar la base de datos |
| mongosh | Incluido con MongoDB | Shell para ejecutar scripts `.js` de consulta e índices |
| mongoimport | MongoDB Database Tools | Carga masiva de datos en formato JSON |
| Python 3 | 3.x | Extracción y transformación de datos desde archivos `.sql` |
| Oracle SQL / SQL Developer | 21c | Base de datos fuente de la fase anterior |

---

## Arquitectura de la Base de Datos

### Modelo Relacional Original (Oracle)

La base de datos en Oracle estaba compuesta por **20 tablas** organizadas en 3 niveles de dependencia:

- **Nivel 1 – Tablas independientes (sin FK):** `Fase`, `Grupo`, `Jugador`, `Mundial`, `Pais`, `Tipo_Premio`, `Tipo_Tarjeta`
- **Nivel 2 – Tablas con 1 FK:** `Premio`, `Red_social`, `Plantilla`, `Llave_Mundial`
- **Nivel 3 – Tablas con 2+ FK:** `Evento_Partido`, `Evento_Cambio_Jugador`, `Pais_Clasificado_Mundial`, `Evento_Falta`, `Evento_Gol`, `Partido_Plantilla`, `Posicion_Jugador`, `Premios_Jugador`, `Cambio_Jugador`

### Modelo Documental en MongoDB

En lugar de replicar las 20 tablas como 20 colecciones, se consolidó toda la información en **3 colecciones principales**, diseñadas en función de las consultas requeridas:

| Colección | Descripción | Consulta que sirve |
|---|---|---|
| `mundiales` | Un documento por cada Mundial, con grupos, partidos, goles, tarjetas, cambios y premios embebidos | Búsqueda por año |
| `jugadores` | Un documento por jugador, con redes sociales embebidas | Catálogo de referencia |
| `paises` | Un documento por país, con historial completo de participaciones | Búsqueda por nombre de país |

Las tablas de catálogo (`Fase`, `Grupo`, `Tipo_Premio`, `Tipo_Tarjeta`) **no se modelan como colecciones independientes**; sus valores se embeben directamente como strings en los documentos que los necesitan, eliminando la necesidad de lookups adicionales durante las consultas.

---

## Diseño del Modelo Documental

### Colección `mundiales`

Cada documento representa un Mundial completo. Agrupa toda la información relacionada con ese torneo, permitiendo responder la consulta por año con un único documento.

```json
{
  "_id": 1,
  "anio": 2022,
  "organizador": "Catar",
  "grupos": [
    {
      "nombre": "A",
      "selecciones": [
        {
          "pais_id": 7,
          "pais": "Argentina",
          "director_tecnico": "Lionel Scaloni"
        }
      ]
    }
  ],
  "partidos": [
    {
      "id_partido": 501,
      "fecha": "2022-11-20",
      "fase": "Grupos",
      "equipo1": { "pais_id": 7, "pais": "Argentina", "plantilla_id": 34 },
      "equipo2": { "pais_id": 21, "pais": "Arabia Saudita", "plantilla_id": 35 },
      "goles": [
        {
          "jugador_id": 1001,
          "jugador": "Messi",
          "minuto": "10",
          "penal": false,
          "entre_tiempo": false
        }
      ],
      "tarjetas": [
        {
          "tipo": "AMARILLA",
          "minuto": "55",
          "entre_tiempo": false
        }
      ],
      "cambios": [
        {
          "jugador_sale_id": 1003,
          "jugador_sale": "Di María",
          "minuto": "70"
        }
      ]
    }
  ],
  "premios": [
    {
      "tipo": "Balón de Oro",
      "pais": "Argentina",
      "entrenador": null,
      "jugadores": ["Messi"]
    }
  ]
}
```

### Colección `jugadores`

Cada documento representa un jugador con sus datos personales y redes sociales embebidas. Este catálogo es referenciado por `jugador_id` dentro de los partidos.

```json
{
  "_id": 1001,
  "nombre": "Lionel Messi",
  "fecha_nacimiento": "1987-06-24",
  "lugar_nacimiento": "Rosario, Argentina",
  "altura": "1.70",
  "apodo": "La Pulga",
  "pagina_web": null,
  "redes_sociales": [
    { "usuario": "@leomessi", "tipo": "Instagram" }
  ]
}
```

### Colección `paises`

Cada documento representa un país con su historial completo de participaciones en mundiales, incluyendo si fue sede y en qué años.

```json
{
  "_id": 7,
  "nombre": "Argentina",
  "participaciones": [
    {
      "mundial_id": 23,
      "anio": 1930,
      "grupo": "1",
      "director_tecnico": "Francisco Olazar",
      "fue_sede": false,
      "anios_sede": []
    },
    {
      "mundial_id": 5,
      "anio": 1978,
      "grupo": "1",
      "director_tecnico": "César Luis Menotti",
      "fue_sede": true,
      "anios_sede": [1978]
    }
  ]
}
```

---

## Configuración del Entorno con Docker

Se utiliza Docker Desktop en Windows para levantar el servidor MongoDB en un contenedor aislado, de la misma forma en que se trabajó con Oracle en fases anteriores.

### Crear el contenedor

Ejecutar el siguiente comando en **PowerShell o CMD**:

```powershell
docker run -d --name mongodb-mundiales `
  -p 27017:27017 `
  -e MONGO_INITDB_ROOT_USERNAME=admin `
  -e MONGO_INITDB_ROOT_PASSWORD=admin123 `
  -v mongodb_mundiales_data:/data/db `
  mongo:latest
```

**Parámetros utilizados:**

| Parámetro | Descripción |
|---|---|
| `--name mongodb-mundiales` | Nombre del contenedor |
| `-p 27017:27017` | Mapeo del puerto de MongoDB al host local |
| `-e MONGO_INITDB_ROOT_USERNAME` | Usuario administrador inicial |
| `-e MONGO_INITDB_ROOT_PASSWORD` | Contraseña del administrador |
| `-v mongodb_mundiales_data:/data/db` | Volumen persistente para los datos |
| `mongo:latest` | Imagen oficial de MongoDB |

### Conectar con MongoDB Compass

Una vez levantado el contenedor, conectarse desde MongoDB Compass usando la siguiente cadena de conexión:

```
mongodb://admin:admin123@localhost:27017
```

---

## Script de Extracción: `parse_inserts.py`

Este script es el primer paso del proceso de migración. Su función es **leer los archivos `.sql` de inserts** generados en Oracle y convertirlos en archivos `.json` individuales, uno por cada tabla original. Estos archivos JSON actúan como los **archivos fuente de carga** requeridos por el enunciado.

### Propósito

Automatizar la transformación de la sintaxis SQL de Oracle (con tipos como `TO_DATE`, `NULL`, comillas simples escapadas con `''`) a objetos JSON válidos que Python y MongoDB puedan procesar.

### Funciones principales

#### `parse_sql_file(filepath)`
Lee el contenido completo de un archivo `.sql` y extrae todas las filas insertadas mediante una expresión regular que identifica el bloque `VALUES (...)` de cada sentencia `INSERT INTO`.  
Retorna una lista de listas, donde cada elemento interno representa los valores de una fila.

#### `parse_values(raw)`
Recibe el contenido crudo de un bloque `VALUES` como string y lo divide en valores individuales, respetando correctamente los strings delimitados por comillas simples que pueden contener comas internas o comillas escapadas con `''` (convención Oracle).  
Retorna una lista de strings con cada valor sin procesar.

#### `clean_value(v)`
Convierte cada valor string extraído al tipo Python correcto:
- `NULL` → `None`
- Strings entre comillas simples → `str` de Python (con el escape `''` resuelto a `'`)
- `TO_DATE('...', '...')` → fecha formateada como `YYYY-MM-DD`
- Valores numéricos → `int` o `float` según corresponda

### Salida generada

El script crea una carpeta `json_output/` y dentro de ella un archivo `.json` por cada tabla procesada:

```
json_output/
├── fase.json
├── grupo.json
├── jugador.json
├── mundial.json
├── pais.json
├── tipo_premio.json
├── tipo_tarjeta.json
├── premio.json
├── red_social.json
├── plantilla.json
├── llave_mundial.json
├── evento_partido.json
├── evento_cambio_jugador.json
├── pais_clasificado_mundial.json
├── evento_falta.json
├── evento_gol.json
├── partido_plantilla.json
├── posicionjugador.json
├── premios_jugador.json
└── cambio_jugador.json
```

### Ejecución

Colocar `parse_inserts.py` en la misma carpeta donde están todos los archivos `.sql` de inserts y ejecutar:

```bash
python parse_inserts.py
```

---

## Script de Transformación: `build_mongo_collections.py`

Este es el script central del proceso. Toma los 20 archivos JSON individuales generados por `parse_inserts.py` y los **ensambla en los 3 documentos de colección** del modelo MongoDB, aplicando toda la lógica de embebido, resolución de IDs y desnormalización.

### Propósito

Construir documentos MongoDB ricos y autosuficientes a partir de los datos relacionales originales, sin perder información y optimizando la estructura para las consultas requeridas.

### Función auxiliar: `load(name)`

Carga un archivo JSON desde la carpeta `json_output/` dado su nombre (sin extensión) y retorna su contenido como lista de diccionarios. Si el archivo no existe, retorna una lista vacía para no interrumpir el proceso.

### Construcción de la colección `jugadores`

1. Se cargan todos los registros de `jugador.json` y `red_social.json`.
2. Se construye un diccionario `redes_por_jugador` que agrupa las redes sociales de cada jugador por su `id_ju`.
3. Para cada jugador, se genera un documento MongoDB con sus datos personales y su lista de redes sociales embebida.

### Construcción de la colección `mundiales`

Este proceso es el más complejo. Antes de iterar por cada mundial, se preparan **mapas auxiliares** (diccionarios Python indexados por ID) para permitir búsquedas en O(1) sin iterar listas completas cada vez:

| Mapa auxiliar | Descripción |
|---|---|
| `pla_por_partido` | Diccionario: `id_partido` → lista de `plantilla_id` que participaron |
| `goles_por_partido` | Diccionario: `id_partido` → lista de goles ocurridos |
| `faltas_por_partido` | Diccionario: `id_partido` → lista de faltas/tarjetas |
| `cambios_por_partido` | Diccionario: `id_partido` → lista de cambios de jugadores |
| `prem_jug_por_premio` | Diccionario: `id_premio` → lista de `jugador_id` ganadores |
| `pcm_por_mundial` | Diccionario: `id_mundial` → lista de países clasificados |
| `premios_por_mundial` | Diccionario: `id_mundial` → lista de premios otorgados |
| `partidos_por_mundial` | Diccionario: `id_mundial` → lista de partidos jugados |

Para cada mundial se construye el documento final con:
- Los **grupos** y sus selecciones, resolviendo el nombre del grupo y el director técnico de la plantilla correspondiente.
- Los **partidos**, incluyendo los dos equipos, goles (con nombre del jugador resuelto), tarjetas y cambios.
- Los **premios**, incluyendo el tipo de premio (resuelto desde el catálogo) y los nombres de los jugadores ganadores.

#### Función interna `equipo_doc(pla_id)`

Recibe el ID de una plantilla y retorna un subdocumento con el `pais_id`, nombre del país y `plantilla_id`, consultando los diccionarios `plantillas` y `paises` para resolver los valores.

### Construcción de la colección `paises`

1. Se construye un diccionario `sedes_por_pais` identificando en qué años cada país fue organizador, cruzando el campo `organizador_mu` de cada mundial con los nombres de países.
2. Se construye `part_por_pais` agrupando todas las participaciones de `pais_clasificado_mundial` por `Pais_id_pa`.
3. Para cada país, se genera un documento con su nombre y la lista de participaciones, indicando en cada una el año, el grupo, el director técnico de su plantilla, y si fue sede y en qué años.

### Salida generada

```
json_output/
├── col_mundiales.json   ← Colección principal para consulta por año
├── col_jugadores.json   ← Catálogo de jugadores con redes sociales
└── col_paises.json      ← Colección principal para consulta por país
```

### Ejecución

```bash
python build_mongo_collections.py
```

---

## Carga de Datos con `mongoimport`

Una vez generados los tres archivos de colecciones, se cargan a MongoDB usando la herramienta `mongoimport`. Cada comando carga una colección completa desde su archivo JSON.

### Opción A: desde la máquina local (requiere MongoDB Database Tools instalado)

```powershell
mongoimport --uri "mongodb://admin:admin123@localhost:27017/mundiales_db?authSource=admin" ^
  --collection mundiales --file json_output/col_mundiales.json --jsonArray

mongoimport --uri "mongodb://admin:admin123@localhost:27017/mundiales_db?authSource=admin" ^
  --collection jugadores --file json_output/col_jugadores.json --jsonArray

mongoimport --uri "mongodb://admin:admin123@localhost:27017/mundiales_db?authSource=admin" ^
  --collection paises --file json_output/col_paises.json --jsonArray
```

### Opción B: desde dentro del contenedor Docker

```powershell
# Copiar los archivos JSON al contenedor
docker cp json_output mongodb-mundiales:/json_output

# Importar cada colección
docker exec -it mongodb-mundiales mongoimport ^
  --username admin --password admin123 ^
  --authenticationDatabase admin ^
  --db mundiales_db --collection mundiales ^
  --file /json_output/col_mundiales.json --jsonArray

docker exec -it mongodb-mundiales mongoimport ^
  --username admin --password admin123 ^
  --authenticationDatabase admin ^
  --db mundiales_db --collection jugadores ^
  --file /json_output/col_jugadores.json --jsonArray

docker exec -it mongodb-mundiales mongoimport ^
  --username admin --password admin123 ^
  --authenticationDatabase admin ^
  --db mundiales_db --collection paises ^
  --file /json_output/col_paises.json --jsonArray
```

---

## Creación de Índices: `setup_indices.js`

Este script es el equivalente al DDL de Oracle para MongoDB. En lugar de definir tablas y restricciones, define los **índices** que permiten que las consultas respondan rápidamente, requisito explícito del enunciado que indica que las consultas no deben tardar en mostrar resultados.

### Ejecución

```bash
mongosh "mongodb://admin:admin123@localhost:27017/mundiales_db" setup_indices.js
```

### Índices creados

#### Sobre la colección `mundiales`

```javascript
// Índice principal: permite buscar un mundial por año en tiempo O(log n)
db.mundiales.createIndex({ anio: 1 }, { unique: true, name: "idx_mundial_anio" });

// Permite filtrar partidos por fase (Grupos, Octavos, Final, etc.)
db.mundiales.createIndex({ "partidos.fase": 1 }, { name: "idx_partido_fase" });

// Permite filtrar selecciones dentro de grupos por nombre de país
db.mundiales.createIndex({ "grupos.selecciones.pais": 1 }, { name: "idx_grupo_pais" });
```

#### Sobre la colección `jugadores`

```javascript
// Permite buscar jugadores por nombre
db.jugadores.createIndex({ nombre: 1 }, { name: "idx_jugador_nombre" });
```

#### Sobre la colección `paises`

```javascript
// Índice principal: permite buscar un país por nombre en tiempo O(log n)
db.paises.createIndex({ nombre: 1 }, { unique: true, name: "idx_pais_nombre" });

// Permite filtrar participaciones por año dentro del documento de un país
db.paises.createIndex({ "participaciones.anio": 1 }, { name: "idx_part_anio" });
```

---

## Métodos de Consulta

Los métodos de consulta son funciones JavaScript ejecutables desde `mongosh`. Son el equivalente a los Stored Procedures de Oracle (`SP_INFO_MUNDIAL` y `Consultar_Historial_Pais`) pero adaptados al paradigma documental de MongoDB.

### Método 1: Consulta por Año del Mundial (`getInfoMundial.js`)

#### Descripción

Recibe como parámetro obligatorio el **año del mundial** y despliega toda la información relacionada: organizador, grupos con sus selecciones y directores técnicos, premios y listado de partidos con goles y resultados. Acepta parámetros opcionales para filtrar por grupo o por país.

#### Parámetros

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `anio` | `Number` | ✅ Sí | Año del mundial a consultar (ej: `2022`) |
| `filtroGrupo` | `String` | ❌ No | Filtrar solo un grupo específico (ej: `"A"`) |
| `filtroPais` | `String` | ❌ No | Filtrar resultados que incluyan a un país (ej: `"Argentina"`) |

#### Lógica interna

1. Busca el documento del mundial usando `db.mundiales.findOne({ anio: anio })`. Gracias al índice `idx_mundial_anio`, esta operación es inmediata.
2. Si se proporcionó `filtroGrupo`, filtra el array `grupos` del documento en memoria.
3. Si se proporcionó `filtroPais`, filtra tanto las selecciones dentro de cada grupo como los partidos donde ese país participó.
4. Imprime los grupos con sus selecciones, los premios del torneo y el detalle de cada partido con goles anotados.

#### Ejemplos de uso

```javascript
// Ver toda la información del Mundial 2022
getInfoMundial(2022);

// Filtrar solo el Grupo A del Mundial 2022
getInfoMundial(2022, "A");

// Ver solo los partidos de Argentina en el Mundial 2022
getInfoMundial(2022, null, "Argentina");

// Combinar filtros: Grupo C con partidos de Polonia
getInfoMundial(2022, "C", "Polonia");
```

#### Ejecución

```bash
mongosh "mongodb://admin:admin123@localhost:27017/mundiales_db" getInfoMundial.js
```

---

### Método 2: Consulta por País (`getHistorialPais.js`)

#### Descripción

Recibe como parámetro el **nombre de un país** y despliega su historial completo en los Mundiales: si fue sede y en qué años, y por cada participación muestra el año, grupo, director técnico y los partidos disputados en ese torneo.

#### Parámetros

| Parámetro | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `nombrePais` | `String` | ✅ Sí | Nombre del país a consultar (ej: `"Brasil"`) |
| `anioFiltro` | `Number` | ❌ No | Filtrar solo la participación de un año específico (ej: `2022`) |

#### Lógica interna

1. Busca el documento del país usando una expresión regular insensible a mayúsculas sobre el campo `nombre`: `db.paises.findOne({ nombre: { $regex: new RegExp(nombrePais, "i") } })`. El índice `idx_pais_nombre` acelera esta búsqueda.
2. Extrae los años en que el país fue sede a partir del campo `anios_sede` en sus participaciones.
3. Si se proporcionó `anioFiltro`, filtra el array `participaciones` para mostrar solo ese año.
4. Para cada participación, realiza una búsqueda secundaria en la colección `mundiales` para obtener los partidos donde el país participó, filtrando por nombre de equipo dentro del array `partidos`.
5. Presenta los resultados ordenados cronológicamente por año.

#### Ejemplos de uso

```javascript
// Ver todo el historial de Brasil en los Mundiales
getHistorialPais("Brasil");

// Ver solo la participación de Argentina en 2022
getHistorialPais("Argentina", 2022);

// Búsqueda parcial (insensible a mayúsculas)
getHistorialPais("alemania");
```

#### Ejecución

```bash
mongosh "mongodb://admin:admin123@localhost:27017/mundiales_db" getHistorialPais.js
```

---

## Estructura de Archivos del Proyecto

```
proyecto-fase3/
│
├── parse_inserts.py                  # Script 1: extrae inserts SQL → JSON individuales
├── build_mongo_collections.py        # Script 2: ensambla los 3 documentos de colección
├── setup_indices.js                  # DDL de MongoDB: crea índices en las colecciones
├── getInfoMundial.js                 # Método de consulta por año del mundial
├── getHistorialPais.js               # Método de consulta por nombre de país
│
├── inserts/                          # Archivos fuente de Oracle (tus .sql originales)
│   ├── fase.sql
│   ├── grupo.sql
│   ├── jugador.sql
│   ├── mundial.sql
│   ├── pais.sql
│   ├── tipo_premio.sql
│   ├── tipo_tarjeta.sql
│   ├── premio.sql
│   ├── red_social.sql
│   ├── plantilla.sql
│   ├── llave_mundial.sql
│   ├── evento_partido.sql
│   ├── evento_cambio_jugador.sql
│   ├── pais_clasificado_mundial.sql
│   ├── evento_falta.sql
│   ├── evento_gol.sql
│   ├── partido_plantilla.sql
│   ├── posicionjugador.sql
│   ├── premios_jugador.sql
│   └── cambio_jugador.sql
│
└── json_output/                      # Generado automáticamente por los scripts Python
    ├── fase.json                     # JSON individuales (archivos fuente de carga)
    ├── grupo.json
    ├── jugador.json
    ├── mundial.json
    ├── pais.json
    ├── tipo_premio.json
    ├── tipo_tarjeta.json
    ├── premio.json
    ├── red_social.json
    ├── plantilla.json
    ├── llave_mundial.json
    ├── evento_partido.json
    ├── evento_cambio_jugador.json
    ├── pais_clasificado_mundial.json
    ├── evento_falta.json
    ├── evento_gol.json
    ├── partido_plantilla.json
    ├── posicionjugador.json
    ├── premios_jugador.json
    ├── cambio_jugador.json
    ├── col_mundiales.json            # Colección final: mundiales
    ├── col_jugadores.json            # Colección final: jugadores
    └── col_paises.json               # Colección final: paises
```

---

## Orden de Ejecución

Seguir estos pasos en orden para reproducir completamente la base de datos:

### Paso 1 — Levantar el contenedor MongoDB

```powershell
docker run -d --name mongodb-mundiales `
  -p 27017:27017 `
  -e MONGO_INITDB_ROOT_USERNAME=admin `
  -e MONGO_INITDB_ROOT_PASSWORD=admin123 `
  -v mongodb_mundiales_data:/data/db `
  mongo:latest
```

Verificar que el contenedor esté corriendo:
```powershell
docker ps
```

### Paso 2 — Extraer los inserts a JSON

Colocar `parse_inserts.py` junto a todos los archivos `.sql` de inserts y ejecutar:

```bash
python parse_inserts.py
```

✅ Se crea la carpeta `json_output/` con 20 archivos JSON individuales.

### Paso 3 — Ensamblar las colecciones MongoDB

```bash
python build_mongo_collections.py
```

✅ Se generan `col_mundiales.json`, `col_jugadores.json` y `col_paises.json` dentro de `json_output/`.

### Paso 4 — Cargar las colecciones a MongoDB

```powershell
docker cp json_output mongodb-mundiales:/json_output

docker exec -it mongodb-mundiales mongoimport --username admin --password admin123 --authenticationDatabase admin --db mundiales_db --collection mundiales --file /json_output/col_mundiales.json --jsonArray

docker exec -it mongodb-mundiales mongoimport --username admin --password admin123 --authenticationDatabase admin --db mundiales_db --collection jugadores --file /json_output/col_jugadores.json --jsonArray

docker exec -it mongodb-mundiales mongoimport --username admin --password admin123 --authenticationDatabase admin --db mundiales_db --collection paises --file /json_output/col_paises.json --jsonArray
```

✅ La base de datos `mundiales_db` queda poblada con las 3 colecciones.

### Paso 5 — Crear los índices

```bash
mongosh "mongodb://admin:admin123@localhost:27017/mundiales_db" setup_indices.js
```

✅ Los índices quedan creados, garantizando consultas rápidas en la defensa.

### Paso 6 — Verificar con MongoDB Compass

Conectarse a `mongodb://admin:admin123@localhost:27017` desde MongoDB Compass y verificar:
- Base de datos: `mundiales_db`
- Colecciones: `mundiales`, `jugadores`, `paises`
- Documentos cargados correctamente en cada colección

### Paso 7 — Probar los métodos de consulta

```bash
mongosh "mongodb://admin:admin123@localhost:27017/mundiales_db" getInfoMundial.js
mongosh "mongodb://admin:admin123@localhost:27017/mundiales_db" getHistorialPais.js
```

✅ El proyecto está listo para la defensa del 25 de abril de 2026.
