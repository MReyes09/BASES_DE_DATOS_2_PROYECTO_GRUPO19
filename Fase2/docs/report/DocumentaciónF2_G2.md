# Documentación Fase 2 - Grupo 19

## Integrantes

| Nombre Completo | Carnet |
|-----------------|--------|
| Daniel Andreé Hernandez Flores | 202300512 |
| Matthew Emmanuel Reyes Melgar | 202202233 |
| Dilan Conaher Suy Miranda | 201801194 |

## Día 1 - 23/03/2026

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

## Día 2 - 24/03/2026

Se crearon datos simulados para verificar el funcionamiento de las triggers y backups.

Primero vamos a demostrar la cantidad de datos que originalmente teníamos en las tablas:

![Count All](./img/05_Initial_Data.png)

Ahora vamos a insertar datos simulados para verificar el funcionamiento de las triggers y el cambio en la base de datos.

Luego de la carga ejecutamos nuevamente el script de verificación de cantidad de datos:

![Count All-Day1](./img/06_Day1_Data.png)

Como podemos notar se aumentaron 15 partidos con varias de sus tablas simuladas en este caso para el Mundial 2026.

Por lo que vamos a proceder a realizar el segundo backup para verificar que el proceso de backup y restore funciona correctamente.

![Backup ejecutado](./img/07_Day1_Full_Backup.png)

## Día - 3 25/03/2026

Se crearon otros 15 partidos con sus respectivas tablas simuladas para verificar el funcionamiento de las triggers y el cambio en la base de datos.

![Count All-Day2](./img/08_Day2_Data.png)

También se realizó su proceso de Full Backup para verificar que el proceso de backup y restore funciona correctamente.

![Backup ejecutado](./img/09_Day2_Full_Backup.png)

## Día - 4 26/03/2026

Se realizó el cambio a UPPER CASE en los nombres de los países para verificar el funcionamiento de las triggers y el cambio en la base de datos.

![Count All-Day3](./img/10_Day3_Data.png)

También se realizó su proceso de Full Backup para verificar que el proceso de backup y restore funciona correctamente.

![Backup ejecutado](./img/11_Day3_Full_Backup.png)