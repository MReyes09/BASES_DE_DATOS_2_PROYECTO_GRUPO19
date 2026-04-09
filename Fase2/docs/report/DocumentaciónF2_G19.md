# Documentación Fase 2 - Grupo 19

## Integrantes

| Nombre Completo | Carnet |
|-----------------|--------|
| Daniel Andreé Hernandez Flores | 202300512 |
| Matthew Emmanuel Reyes Melgar | 202202233 |
| Dilan Conaher Suy Miranda | 201801194 |

<!-- ========== INICIO SECCIÓN AGREGADA ========== -->

## Especificaciones Técnicas del Servidor

El proyecto fue ejecutado en un contenedor Docker con Oracle Database, con las
siguientes especificaciones de hardware y software:

| Componente | Detalle |
|------------|---------|
| **Motor de Base de Datos** | Oracle AI Database 26ai Free Release 23.26.1.0.0 |
| **Entorno** | Contenedor Docker (overlay filesystem) |
| **Sistema Operativo** | Oracle Linux (imagen oficial Oracle Database Free) |
| **RAM** | 11.5 GB |
| **CPU** | 12 núcleos |
| **Almacenamiento total** | 1,007 GB |
| **Almacenamiento disponible** | 929 GB |
| **Herramienta de backup** | RMAN (Recovery Manager) — línea de comandos |
| **Modo de base de datos** | ARCHIVELOG |
| **PDB utilizado** | freePDB1 |

---

## Plan de Respaldo

### Estrategia elegida

Se implementaron dos estrategias de respaldo de forma paralela durante los mismos
días de carga:

1. **Full Backup (Backup Completo):** copia íntegra de todos los bloques de la base
   de datos al final de cada día de carga.
2. **Incremental Backup (RMAN Level 0 + Level 1):** un backup base (Level 0) al inicio,
   seguido de backups diferenciales (Level 1) al final de cada día, capturando únicamente
   los bloques modificados desde el último backup.

### Justificación de la elección

Oracle Database 21c/23ai soporta nativamente el backup incremental mediante RMAN,
lo que lo hace la opción más eficiente frente al diferencial en términos de espacio y
velocidad. Se descartó `expdp` (Data Pump) ya que exporta datos a texto plano, lo cual
no cumple con los requerimientos técnicos del enunciado.

### Cronograma de respaldos ejecutados

| Día | Fecha | Operación | Full Backup | Incremental |
|-----|-------|-----------|-------------|-------------|
| Día 0 | 23/03/2026 | Carga base Fase 1 + tablas LOG | ✅ FULL_DAY1 | ✅ INCR_L0_BASE |
| Día 1 | 25/03/2026 | Inserción 15 partidos (ronda 1) | ✅ FULL_DAY2 | ✅ INCR_L1_DIA1 |
| Día 2 | 28/03/2026 | Inserción 15 partidos (ronda 2) | ✅ FULL_DAY3 | ✅ INCR_L1_DIA2 |
| Día 3 | 30/03/2026 | UPDATE países a MAYÚSCULAS | ✅ FULL_DAY4 | ✅ INCR_L1_DIA3 |

### Rutas de almacenamiento

Los backups fueron almacenados en el área de recuperación configurada en Oracle:

```sql
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST_SIZE = 10G SCOPE=BOTH;
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST = '/opt/oracle/recovery_area' SCOPE=BOTH;
```

<!-- ========== FIN SECCIÓN AGREGADA ========== -->

---

## Full Backup

### Día 1 - 23/03/2026

Como bien se describe en el enunciado, lo primero que hicimos fue alterar el script de la creación de la base de datos, esto con el fin de agregar las tablas de log y las triggers correspondientes para cada tabla.

Tenemos esta estructura de tablas de log:

**TABLAS DE LOG (Registro / Bitacora)**
- Cada tabla LOG almacena:
  - log_id:         Identificador unico autogenerado
  - log_operacion:  Tipo de operacion (INSERT, UPDATE, DELETE)
  - log_fecha:      Fecha y hora de la operacion
  - log_usuario:    Usuario que realizo la operacion
  - Todas las columnas de la tabla original (sin constraints)

![Estructura de tablas de log](./img/01_DDL_Logs.png)

>**NOTA:** Se creó otro usuario con los privilegios necesarios para poder realizar las pruebas de las triggers y además para que pudiera acceder a la configuración de Backups, ya que Oracle maneja la seguridad de los usuarios de manera diferente, por lo tanto es un nuevo esquema.

```sql
-- USER SQL
-- Creamos el usuario (cambia 'usuario_juego' y el password por los que prefieras)
CREATE USER BD2_P1_F2 IDENTIFIED BY "12345";

-- QUOTAS
-- Le damos espacio de almacenamiento ilimitado en el disco por defecto para que guarde sus tablas
ALTER USER BD2_P1_F2 QUOTA UNLIMITED ON USERS;

-- ROLES
-- CONNECT: Para iniciar sesión. RESOURCE: Para crear objetos básicos de desarrollo.
GRANT CONNECT, RESOURCE TO BD2_P1_F2;

-- SYSTEM PRIVILEGES
-- Permisos explícitos de desarrollo
GRANT CREATE SESSION TO BD2_P1_F2;
GRANT CREATE TABLE TO BD2_P1_F2;
GRANT CREATE TRIGGER TO BD2_P1_F2;
GRANT CREATE VIEW TO BD2_P1_F2;
GRANT CREATE SEQUENCE TO BD2_P1_F2;

-- EL PERMISO PARA HACER BACKUPS (RMAN)
GRANT SYSDBA TO BD2_P1_F2;
```

Luego de eso se ejecutaron los scripts de creación de tablas y triggers, y se realizaron las pruebas de las triggers para verificar que funcionaban correctamente. También se hizo la carga de la data desde los inserts generados en la fase 1.

Se procedió con la ejecución de un Backup solo para familiarizarnos con el proceso de backup y restore en Oracle Database 21c.

Crear el Script sqldev.rman

![Backup ejecutado](./img/02_Backup-Full.png)

Este paso depende, pero se ejecuta dentro de la máquina local o en algunos casos, dentro de docker

Pero lo importante es ejecutar el script sqldev.rman

```bash
rman target / @/tmp/sqldev.rman
```

![Backup ejecutado](./img/03_Succes_Full_Backup.png)

El proceso fue bastante rápido, durando aproximadamente 1 minuto.

Y pudimos verificar que el backup se creó correctamente.


```sql
SELECT 
    piece#, 
    handle AS ruta_del_archivo, 
    completion_time AS fecha_finalizacion, 
    status
FROM 
    v$backup_piece 
ORDER BY 
    completion_time DESC;
```

![Backup ejecutado](./img/04_Verify_Status.png)

### Día 2 - 24/03/2026

Se crearon datos simulados para verificar el funcionamiento de las triggers y backups.

Primero vamos a demostrar la cantidad de datos que originalmente teníamos en las tablas:

![Count All](./img/05_Initial_Data.png)

Ahora vamos a insertar datos simulados para verificar el funcionamiento de las triggers y el cambio en la base de datos.

Luego de la carga ejecutamos nuevamente el script de verificación de cantidad de datos:

![Count All-Day1](./img/06_Day1_Data.png)

Como podemos notar se aumentaron 15 partidos con varias de sus tablas simuladas en este caso para el Mundial 2026.

Por lo que vamos a proceder a realizar el segundo backup para verificar que el proceso de backup y restore funciona correctamente.

![Backup ejecutado](./img/07_Day1_Full_Backup.png)

### Día - 3 25/03/2026

Se crearon otros 15 partidos con sus respectivas tablas simuladas para verificar el funcionamiento de las triggers y el cambio en la base de datos.

![Count All-Day2](./img/08_Day2_Data.png)

También se realizó su proceso de Full Backup para verificar que el proceso de backup y restore funciona correctamente.

![Backup ejecutado](./img/09_Day2_Full_Backup.png)

### Día - 4 26/03/2026

Se realizó el cambio a UPPER CASE en los nombres de los países para verificar el funcionamiento de las triggers y el cambio en la base de datos.

![Count All-Day3](./img/10_Day3_Data.png)

También se realizó su proceso de Full Backup para verificar que el proceso de backup y restore funciona correctamente.

![Backup ejecutado](./img/11_Day3_Full_Backup.png)


## Incremental Backup

### Configuración Previa

Antes de iniciar el proceso de backup incremental, se verificó que la base de datos 
estuviera en modo ARCHIVELOG (requisito para RMAN) y se configuró el área de recuperación:

```sql
SELECT LOG_MODE FROM V$DATABASE;
-- Resultado: ARCHIVELOG ✅

ALTER SYSTEM SET DB_RECOVERY_FILE_DEST_SIZE = 10G SCOPE=BOTH;
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST = '/opt/oracle/recovery_area' SCOPE=BOTH;
```

También fue necesario abrir el PDB correctamente y guardar su estado para que 
persista entre reinicios:

```sql
ALTER PLUGGABLE DATABASE freePDB1 OPEN;
ALTER PLUGGABLE DATABASE freePDB1 SAVE STATE;
```

### Día 0 - 23/03/2026 (LEVEL 0 - Backup Base)

Se realizó la carga completa de la data base (Fase 1) con COMMIT confirmado, 
y se tomó el backup incremental LEVEL 0, que sirve como fotografía base para 
los incrementales posteriores.

Script ejecutado (`backup_incr_level0.rman`):

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
BACKUP INCREMENTAL LEVEL 0 DEVICE TYPE DISK TAG 'INCR_L0_BASE' DATABASE;
BACKUP DEVICE TYPE DISK TAG 'ARCH_L0_BASE' ARCHIVELOG ALL NOT BACKED UP;
ALTER DATABASE OPEN;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

```bash
rman target / @/opt/oracle/backup_incr_level0.rman
```

![Backup Level 0 ejecutado](./img/Day0_Nivel0_time_increment.png)

Verificación del backup y estado inicial de la base de datos:

![Verificación Level 0](./img/Day0_Backup_RMAN_Base_Increment.png)

![Count tablas Day0](./img/Day0_Count_increment.png)

### Día 1 - 25/03/2026 (LEVEL 1 - Dieciseisavos)

Se cargaron 15 partidos de dieciseisavos de final con sus respectivos goles, 
faltas y cambios de jugador (IDs Evento_Partido 965–979).

Script ejecutado (`backup_incr_dia1.rman`):

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
BACKUP INCREMENTAL LEVEL 1 DEVICE TYPE DISK TAG 'INCR_L1_DIA1' DATABASE;
BACKUP DEVICE TYPE DISK TAG 'ARCH_L1_DIA1' ARCHIVELOG ALL NOT BACKED UP;
ALTER DATABASE OPEN;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

![Count tablas Day1](./img/Day1_LoadData_Increment.png)

![Backup Level 1 Día 1](./img/Day1_Backup_RMAN_increment.png)

### Día 2 - 28/03/2026 (LEVEL 1 - Eliminatorias)

Se cargaron 15 partidos adicionales correspondientes a Octavos, Cuartos, 
Semifinales y Final (IDs Evento_Partido 980–994).

![Count tablas Day2](./img/Day2_LoadData_increment.png)

![Backup Level 1 Día 2](./img/Day2_Backup_RMAN_increment.png)

### Día 3 - 30/03/2026 (LEVEL 1 - UPDATE Países)

Este día no hubo inserts, sino un UPDATE masivo que convirtió todos los 
nombres de países a MAYÚSCULAS para verificar que los backups incrementales 
capturan cambios de tipo UPDATE correctamente.

![Países en mayúsculas](./img/Day3_updateData_Increment.png)

![Backup Level 1 Día 3](./img/Day3_Backup_RMAN_increment.png)

<!-- ========== INICIO SECCIÓN AGREGADA ========== -->
## Restauración Full Backup

### Preparación — Eliminación de la Base de Datos

Antes de iniciar el proceso de restauración de los Full Backups, se eliminaron todas las 
tablas del esquema `BD2_P1_F2` para simular un escenario de pérdida total de datos y 
demostrar que los backups pueden recuperar la información de forma completa.

```sql
-- Verificación del estado antes de eliminar
SELECT table_name FROM all_tables WHERE owner = 'BD2_P1_F2';
```

![Estado de la BD antes del DROP](./img/Full_Restore_Before_Drop.png) <!-- PENDIENTE: captura -->

Se ejecutó el DROP en cascada sobre todas las tablas del esquema:

```sql
BEGIN
  FOR t IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/
```

![Tablas eliminadas](./img/Full_Restore_Drop_DB.png) <!-- PENDIENTE: captura -->

Se verificó que el esquema quedara vacío antes de proceder con la restauración:

![Verificación esquema vacío](./img/Full_Restore_Empty_Schema.png) <!-- PENDIENTE: captura -->

---

### Restauración Full Backup — Día 4 (26/03/2026)

Se restauró el último full backup, correspondiente al estado final de la base de datos 
con los 30 partidos simulados cargados y los nombres de países en MAYÚSCULAS. 
Este backup representa el estado más reciente y completo de los datos.

Script de restauración (`restore_full.rman`):

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
RESTORE DATABASE FROM TAG 'FULL_DAY4';
RECOVER DATABASE;
ALTER DATABASE OPEN RESETLOGS;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

```bash
time rman target / @/opt/oracle/restore_full_day4.rman
```

![Restauración Full Backup](./img/Full_Restore_Day4_Execute.png) <!-- PENDIENTE: captura -->

![Tiempo restauración Full Backup](./img/Full_Restore_Day4_Time.png) <!-- PENDIENTE: captura -->

Validación post-restauración:

![Validación datos Day4 — Demostración de datos restaurados](./img/Full_Restore_Day4_Count.png) <!-- PENDIENTE: captura -->

---

### Resumen de Tiempos — Restauración Full Backup

| Backup | Fecha | Tag | Datos en BD | Tiempo de Restauración |
|--------|-------|-----|-------------|------------------------|
| Full Día 4 | 26/03/2026 | FULL_DAY4 | 30 partidos + países MAYÚSCULAS | ~17 seg |

> Ver análisis comparativo con el incremental en la sección de Conclusiones.

<!-- ========== FIN SECCIÓN AGREGADA ========== -->

---

### Restauración Incremental

Para simular un desastre, se ejecutó DROP TABLE en cascada sobre todas las 
tablas del esquema BASES2_PROYECTO. Luego se procedió con la restauración 
usando point-in-time recovery para recuperar el estado exacto del Día 3, 
excluyendo los DROP TABLE posteriores.

Script de restauración (`restore_incremental.rman`):

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
RESTORE DATABASE UNTIL TIME 
  "TO_DATE('2026-03-31 23:59:59','YYYY-MM-DD HH24:MI:SS')";
RECOVER DATABASE UNTIL TIME 
  "TO_DATE('2026-03-31 23:59:59','YYYY-MM-DD HH24:MI:SS')";
ALTER DATABASE OPEN RESETLOGS;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

RMAN aplicó automáticamente los backups en orden secuencial:
1. INCR_L0_BASE (base)
2. INCR_L1_DIA1
3. INCR_L1_DIA2
4. INCR_L1_DIA3

**Tiempo de restauración: ~6 segundos**

![Restore ejecutado](./img/restore_incremental_time.png)

Verificación post-restauración — datos recuperados con países en MAYÚSCULAS:

![Verificación post-restore](./img/restore_prints.png)

<!-- ========== INICIO SECCIÓN AGREGADA ========== -->

---

## Análisis Comparativo de Estrategias de Backup

### Tiempos de Restauración

A continuación se comparan los tiempos de restauración obtenidos durante las pruebas
de recuperación para ambas estrategias:

| Estrategia | Backups involucrados | Datos recuperados | Tiempo de restauración |
|------------|---------------------|-------------------|------------------------|
| Full Backup | 1 archivo (FULL_DAY4) | Estado completo Día 4 | **~17 segundos** |
| Incremental Backup | 4 archivos (L0 + L1×3) | Estado completo Día 3 | **~6 segundos** |

### Evidencia de tiempos

**Full Backup — 17 segundos:**

![Tiempo restauración Full Backup](./img/Full_Restore_Day4_Time.png)

**Incremental Backup — 6 segundos:**

![Tiempo restauración Incremental](./img/restore_incremental_time.png)

### Análisis de Resultados

**Full Backup:**
- Restauración en un solo paso, sin dependencia entre archivos
- Tiempo mayor (~17s) porque debe restaurar el volumen completo de datos en un solo archivo
- Proceso simple y directo: un archivo → un restore
- Mayor tamaño de almacenamiento requerido por backup

**Incremental Backup:**
- Restauración más rápida (~6s) porque cada archivo incremental solo contiene los cambios del día
- Requiere aplicar los backups en orden secuencial (L0 → L1 Día1 → L1 Día2 → L1 Día3)
- Menor espacio de almacenamiento al acumular solo los deltas entre días
- Mayor complejidad en la gestión de la cadena de backups

### Tabla Comparativa General

| Criterio | Full Backup | Incremental Backup |
|----------|-------------|-------------------|
| Tiempo de restauración | ~17 segundos | ~6 segundos |
| Archivos necesarios para restaurar | 1 | 4 (L0 + 3×L1) |
| Espacio en disco por backup | Mayor | Menor |
| Complejidad de restauración | Baja | Media |
| Riesgo de falla en cadena | Ninguno | Si falla un L1, afecta los siguientes |
| Point-in-time recovery | No (estado fijo) | Sí (hasta un timestamp exacto) |

---

## Conclusiones

### ¿Qué estrategia recomendamos?

Para el volumen de datos manejado en este proyecto (base de datos del Mundial 2026 con
datos de partidos, goles, faltas y cambios de jugador), **recomendamos el Incremental Backup**
como estrategia principal, complementado con un Full Backup periódico como base.

### Justificación

1. **Velocidad de restauración:** El incremental demostró ser **2.8 veces más rápido** (6s vs 17s).
   En un ambiente de producción, cada segundo de downtime tiene un costo operativo real.

2. **Eficiencia de almacenamiento:** Los backups incrementales almacenan únicamente los
   cambios ocurridos desde el último backup, reduciendo significativamente el espacio requerido
   en disco cuando los volúmenes de datos son grandes.

3. **Point-in-time recovery:** El incremental permite recuperar la base de datos a un
   momento exacto en el tiempo, lo cual es crítico cuando se necesita excluir operaciones
   erróneas (como un DROP TABLE accidental) sin perder todo el trabajo posterior.

4. **Escalabilidad:** A medida que la base de datos crece, la ventaja del incremental se
   amplifica: el full backup crece proporcionalmente con los datos, mientras que el
   incremental solo crece con los cambios diarios.

### Cuándo usar cada estrategia

| Escenario | Estrategia recomendada |
|-----------|------------------------|
| Base de datos pequeña, restauración simple | Full Backup |
| Base de datos grande con cambios diarios | Incremental como base |
| Necesidad de restaurar a un momento exacto | Incremental (point-in-time) |
| Estrategia combinada (producción real) | Full semanal + Incremental diario |

En un entorno empresarial real, la mejor práctica es combinar ambas estrategias:
un **Full Backup semanal** como punto de referencia seguro, y **backups incrementales diarios**
para minimizar el tiempo de restauración y el espacio consumido.

<!-- ========== FIN SECCIÓN AGREGADA ========== -->