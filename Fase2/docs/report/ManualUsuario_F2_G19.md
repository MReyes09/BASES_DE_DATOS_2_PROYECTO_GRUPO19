# Manual de Usuario — Respaldo y Restauración de Base de Datos
### Fase 2 - Grupo 19

---

## Integrantes

| Nombre Completo | Carnet |
|-----------------|--------|
| Daniel Andreé Hernandez Flores | 202300512 |
| Matthew Emmanuel Reyes Melgar | 202202233 |
| Dilan Conaher Suy Miranda | 201801194 |

---

## Índice

1. [Requisitos Previos](#1-requisitos-previos)
2. [Configuración del Entorno](#2-configuración-del-entorno)
3. [Cómo Realizar un Full Backup](#3-cómo-realizar-un-full-backup)
4. [Cómo Realizar un Incremental Backup](#4-cómo-realizar-un-incremental-backup)
5. [Cómo Restaurar desde un Full Backup](#5-cómo-restaurar-desde-un-full-backup)
6. [Cómo Restaurar desde un Incremental Backup](#6-cómo-restaurar-desde-un-incremental-backup)
7. [Interpretación de Registros de Respaldo](#7-interpretación-de-registros-de-respaldo)
8. [Procedimientos de Validación Post-Restauración](#8-procedimientos-de-validación-post-restauración)
9. [Solución de Problemas Comunes](#9-solución-de-problemas-comunes)

---

## 1. Requisitos Previos

Antes de ejecutar cualquier backup o restauración, verificar que se cumplan los siguientes requisitos:

### Software necesario
- Oracle Database 23ai Free (o versión compatible)
- Acceso a RMAN desde línea de comandos
- Usuario con privilegios `SYSDBA`

### Verificar que la base de datos está en modo ARCHIVELOG

Conectarse como SYSDBA y ejecutar:

```sql
SELECT LOG_MODE FROM V$DATABASE;
```

El resultado debe ser:
```
LOG_MODE
------------
ARCHIVELOG
```

> Si el resultado es `NOARCHIVELOG`, los backups incrementales no funcionarán. Activar ARCHIVELOG con:
> ```sql
> SHUTDOWN IMMEDIATE;
> STARTUP MOUNT;
> ALTER DATABASE ARCHIVELOG;
> ALTER DATABASE OPEN;
> ```

### Verificar que el PDB está abierto

```sql
SELECT name, open_mode FROM v$pdbs;
```

El PDB `FREEPDB1` debe mostrar `READ WRITE`. Si no, abrirlo:

```sql
ALTER PLUGGABLE DATABASE freePDB1 OPEN;
ALTER PLUGGABLE DATABASE freePDB1 SAVE STATE;
```

---

## 2. Configuración del Entorno

### Configurar el área de recuperación (Recovery Area)

Ejecutar como SYSDBA:

```sql
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST_SIZE = 10G SCOPE=BOTH;
ALTER SYSTEM SET DB_RECOVERY_FILE_DEST = '/opt/oracle/recovery_area' SCOPE=BOTH;
```

### Verificar la configuración

```sql
SHOW PARAMETER DB_RECOVERY_FILE_DEST;
```

### Conectarse a RMAN

```bash
rman target /
```

Si la conexión fue exitosa verás:
```
Recovery Manager: Release 23.0.0.0.0
connected to target database: FREE (DBID=...)
```

---

## 3. Cómo Realizar un Full Backup

Un Full Backup copia todos los bloques de la base de datos. Debe ejecutarse al final de cada día de carga.

### Paso 1 — Crear el script RMAN

Crear el archivo `/opt/oracle/backup_full_dayX.rman` con el siguiente contenido:

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
BACKUP DATABASE TAG 'FULL_DAYX';
BACKUP ARCHIVELOG ALL NOT BACKED UP TAG 'ARCH_FULL_DAYX';
ALTER DATABASE OPEN;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

> Reemplazar `X` con el número del día correspondiente (1, 2, 3, 4).

### Paso 2 — Ejecutar el script

```bash
time rman target / @/opt/oracle/backup_full_dayX.rman
```

El comando `time` mide el tiempo total de ejecución (valor `real` al final).

### Paso 3 — Verificar que el backup se creó correctamente

Conectarse a SQL*Plus y ejecutar:

```sql
SELECT 
    piece#,
    handle AS ruta_archivo,
    completion_time AS fecha_fin,
    status
FROM v$backup_piece
ORDER BY completion_time DESC;
```

El campo `STATUS` debe mostrar `A` (Available).

---

## 4. Cómo Realizar un Incremental Backup

El incremental se divide en dos tipos:
- **Level 0:** backup base completo (se hace una sola vez al inicio)
- **Level 1:** backup de los bloques modificados desde el último backup (se hace cada día)

### 4.1 Backup Incremental Level 0 (solo el primer día)

Crear `/opt/oracle/backup_incr_level0.rman`:

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
BACKUP INCREMENTAL LEVEL 0 DEVICE TYPE DISK TAG 'INCR_L0_BASE' DATABASE;
BACKUP DEVICE TYPE DISK TAG 'ARCH_L0_BASE' ARCHIVELOG ALL NOT BACKED UP;
ALTER DATABASE OPEN;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

Ejecutar:

```bash
time rman target / @/opt/oracle/backup_incr_level0.rman
```

### 4.2 Backup Incremental Level 1 (días siguientes)

Crear `/opt/oracle/backup_incr_diaX.rman`:

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
BACKUP INCREMENTAL LEVEL 1 DEVICE TYPE DISK TAG 'INCR_L1_DIAX' DATABASE;
BACKUP DEVICE TYPE DISK TAG 'ARCH_L1_DIAX' ARCHIVELOG ALL NOT BACKED UP;
ALTER DATABASE OPEN;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

Ejecutar:

```bash
time rman target / @/opt/oracle/backup_incr_diaX.rman
```

### 4.3 Verificar backups incrementales generados

```sql
SELECT 
    backup_type,
    incremental_level,
    tag,
    start_time,
    completion_time,
    status
FROM v$backup_set
ORDER BY start_time DESC;
```

---

## 5. Cómo Restaurar desde un Full Backup

### Paso 1 — Eliminar la base de datos actual (simulación de desastre)

Conectarse al esquema y ejecutar:

```sql
BEGIN
  FOR t IN (SELECT table_name FROM user_tables) LOOP
    EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS';
  END LOOP;
END;
/
```

Verificar que el esquema quedó vacío:

```sql
SELECT COUNT(*) FROM user_tables;
-- Debe retornar 0
```

### Paso 2 — Crear el script de restauración

Crear `/opt/oracle/restore_full_dayX.rman`:

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
RESTORE DATABASE FROM TAG 'FULL_DAYX';
RECOVER DATABASE;
ALTER DATABASE OPEN RESETLOGS;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

### Paso 3 — Ejecutar la restauración midiendo el tiempo

```bash
time rman target / @/opt/oracle/restore_full_dayX.rman
```

### Paso 4 — Validar la restauración

Ver sección [8. Procedimientos de Validación Post-Restauración](#8-procedimientos-de-validación-post-restauración).

---

## 6. Cómo Restaurar desde un Incremental Backup

La restauración incremental usa **point-in-time recovery**, lo que permite recuperar la base de datos al estado exacto de una fecha y hora específica.

### Paso 1 — Eliminar la base de datos actual

Mismo procedimiento que en la sección 5, Paso 1.

### Paso 2 — Crear el script de restauración

Crear `/opt/oracle/restore_incremental.rman`, especificando la fecha/hora hasta la que se desea restaurar:

```bash
SHUTDOWN IMMEDIATE;
STARTUP MOUNT;
RESTORE DATABASE UNTIL TIME
  "TO_DATE('YYYY-MM-DD HH24:MI:SS','YYYY-MM-DD HH24:MI:SS')";
RECOVER DATABASE UNTIL TIME
  "TO_DATE('YYYY-MM-DD HH24:MI:SS','YYYY-MM-DD HH24:MI:SS')";
ALTER DATABASE OPEN RESETLOGS;
ALTER PLUGGABLE DATABASE ALL OPEN;
```

> Reemplazar `YYYY-MM-DD HH24:MI:SS` con la fecha/hora objetivo.
> Ejemplo para recuperar hasta el 31 de marzo de 2026 a las 23:59:59:
> `"TO_DATE('2026-03-31 23:59:59','YYYY-MM-DD HH24:MI:SS')"`

### Paso 3 — Ejecutar la restauración

```bash
time rman target / @/opt/oracle/restore_incremental.rman
```

RMAN aplicará automáticamente los backups en orden:
1. `INCR_L0_BASE` (base completa)
2. `INCR_L1_DIA1` (cambios Día 1)
3. `INCR_L1_DIA2` (cambios Día 2)
4. `INCR_L1_DIA3` (cambios Día 3)

### Paso 4 — Validar la restauración

Ver sección [8. Procedimientos de Validación Post-Restauración](#8-procedimientos-de-validación-post-restauración).

---

## 7. Interpretación de Registros de Respaldo

### 7.1 Log de RMAN durante el backup

Durante la ejecución de un backup, RMAN muestra mensajes como:

```
Starting backup at 26-MAR-26
allocated channel: ORA_DISK_1
channel ORA_DISK_1: SID=XX device type=DISK
channel ORA_DISK_1: starting full datafile backup set
channel ORA_DISK_1: specifying datafile(s) in backup set
...
channel ORA_DISK_1: backup set complete, elapsed time: 00:00:17
Finished backup at 26-MAR-26
```

| Campo | Significado |
|-------|-------------|
| `Starting backup at` | Fecha y hora de inicio del backup |
| `allocated channel` | Canal de disco asignado para escribir el backup |
| `elapsed time` | Tiempo total que tomó el backup |
| `Finished backup at` | Fecha y hora de finalización |

### 7.2 Consultar el historial de backups

```sql
SELECT 
    operation,
    status,
    start_time,
    end_time,
    (end_time - start_time) * 86400 AS duracion_segundos
FROM v$rman_status
WHERE operation IN ('BACKUP', 'RESTORE', 'RECOVER')
ORDER BY start_time DESC;
```

### 7.3 Estados posibles en v$backup_piece

| Status | Significado |
|--------|-------------|
| `A` | Available — backup disponible y utilizable |
| `D` | Deleted — backup eliminado |
| `X` | Expired — backup ya no existe en disco |

### 7.4 Verificar integridad de un backup sin restaurar

```bash
rman target /
VALIDATE BACKUPSET TAG='FULL_DAY4';
```

Si no hay errores, el backup es válido para restaurar.

---

## 8. Procedimientos de Validación Post-Restauración

Después de cualquier restauración (full o incremental), ejecutar los siguientes pasos para confirmar que los datos se recuperaron correctamente.

### Paso 1 — Verificar que el PDB está abierto

```sql
SELECT name, open_mode FROM v$pdbs;
-- Debe mostrar READ WRITE
```

### Paso 2 — Contar registros por tabla principal

Conectarse al esquema restaurado y ejecutar:

```sql
SELECT 'PAIS' AS tabla, COUNT(*) AS total FROM PAIS
UNION ALL
SELECT 'EQUIPO', COUNT(*) FROM EQUIPO
UNION ALL
SELECT 'JUGADOR', COUNT(*) FROM JUGADOR
UNION ALL
SELECT 'PARTIDO', COUNT(*) FROM PARTIDO
UNION ALL
SELECT 'EVENTO_PARTIDO', COUNT(*) FROM EVENTO_PARTIDO
UNION ALL
SELECT 'GOL', COUNT(*) FROM GOL
UNION ALL
SELECT 'FALTA', COUNT(*) FROM FALTA
UNION ALL
SELECT 'CAMBIO_JUGADOR', COUNT(*) FROM CAMBIO_JUGADOR;
```

Los conteos deben coincidir exactamente con los registrados antes de eliminar la base de datos.

### Paso 3 — Verificar integridad de datos específicos

Para el backup del Día 4 (países en MAYÚSCULAS):

```sql
SELECT pais_nombre FROM PAIS WHERE ROWNUM <= 5;
-- Todos los nombres deben aparecer en MAYÚSCULAS
```

### Paso 4 — Verificar tablas de LOG

```sql
SELECT 'LOG_PAIS' AS tabla, COUNT(*) AS total FROM LOG_PAIS
UNION ALL
SELECT 'LOG_PARTIDO', COUNT(*) FROM LOG_PARTIDO
UNION ALL
SELECT 'LOG_JUGADOR', COUNT(*) FROM LOG_JUGADOR;
```

Las tablas de log deben contener los registros de todas las operaciones realizadas.

### Checklist de validación

| Verificación | Comando | Resultado esperado |
|--------------|---------|-------------------|
| PDB abierto | `SELECT open_mode FROM v$pdbs` | `READ WRITE` |
| Tablas existentes | `SELECT COUNT(*) FROM user_tables` | Mismo número que antes |
| Conteo de datos | `SELECT COUNT(*) FROM PARTIDO` | Coincide con original |
| Logs activos | `SELECT COUNT(*) FROM LOG_PAIS` | Mayor a 0 |
| Datos correctos | `SELECT * FROM PAIS WHERE ROWNUM <= 3` | Datos íntegros |

---

## 9. Solución de Problemas Comunes

### Error: ORA-19870 — backup piece not found

**Causa:** El archivo de backup fue movido o eliminado del disco.

**Solución:**
```bash
rman target /
CROSSCHECK BACKUP;
DELETE EXPIRED BACKUP;
```

---

### Error: ORA-01152 — file was not restored from a sufficiently old backup

**Causa:** El backup usado es más antiguo que los redo logs disponibles.

**Solución:** Usar `RESETLOGS` al abrir la base de datos:
```bash
ALTER DATABASE OPEN RESETLOGS;
```

---

### Error: RMAN-06026 — some targets not found

**Causa:** El TAG especificado en el script no existe.

**Solución:** Verificar los TAGs disponibles:
```sql
SELECT tag, status FROM v$backup_set ORDER BY start_time DESC;
```

---

### La base de datos no abre después de restaurar

**Solución paso a paso:**
```sql
-- 1. Verificar el estado
SELECT status FROM v$instance;

-- 2. Si está en MOUNT, intentar abrir
ALTER DATABASE OPEN RESETLOGS;

-- 3. Abrir el PDB
ALTER PLUGGABLE DATABASE ALL OPEN;
```

---

*Manual de Usuario — Bases de Datos 2, Fase 2, Grupo 19 — 2026*
