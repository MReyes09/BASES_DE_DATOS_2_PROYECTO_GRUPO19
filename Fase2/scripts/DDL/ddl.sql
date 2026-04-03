-- Generado por Oracle SQL Developer Data Modeler 24.3.1.351.0831
--   en:        2026-03-15 19:40:23 CST
--   sitio:      Oracle Database 21c
--   tipo:      Oracle Database 21c



-- predefined type, no DDL - MDSYS.SDO_GEOMETRY

-- predefined type, no DDL - XMLTYPE

CREATE TABLE Cambio_Jugador
    (
     id_ca_ju                          NUMBER  NOT NULL ,
     Evento_Cambio_Jugador_id_ev_ca_ju NUMBER  NOT NULL ,
     Jugador_id_ju                     NUMBER  NOT NULL ,
     tiempo_ca_ju                      VARCHAR2 (8)
    )
    LOGGING
;

ALTER TABLE Cambio_Jugador
    ADD CONSTRAINT Cambio_Jugador_PK PRIMARY KEY ( id_ca_ju ) ;

CREATE TABLE Evento_Cambio_Jugador 
    ( 
     id_ev_ca_ju             NUMBER  NOT NULL , 
     Evento_Partido_id_ev_pa NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Evento_Cambio_Jugador 
    ADD CONSTRAINT Evento_Cambio_Jugador_PK PRIMARY KEY ( id_ev_ca_ju ) ;

CREATE TABLE Evento_Falta
    (
     id_ev_fa                NUMBER  NOT NULL ,
     Evento_Partido_id_ev_pa NUMBER  NOT NULL ,
     Tipo_Tarjeta_id_ti_ta   NUMBER  NOT NULL ,
     minuto_falta            VARCHAR2 (8)  NOT NULL ,
     entre_tiempo            NUMBER  NOT NULL
    )
    LOGGING
;

ALTER TABLE Evento_Falta
    ADD CONSTRAINT Evento_Falta_PK PRIMARY KEY ( id_ev_fa ) ;

CREATE TABLE Evento_Gol 
    ( 
     id_ev_go                NUMBER  NOT NULL , 
     Evento_Partido_id_ev_pa NUMBER  NOT NULL , 
     Jugador_id_ju           NUMBER  NOT NULL , 
     tiempo_gol              VARCHAR2 (8)  NOT NULL , 
     entre_tiempo_ev_go      VARCHAR2 (8) , 
     penal                   NUMBER 
    ) 
    LOGGING 
;

ALTER TABLE Evento_Gol 
    ADD CONSTRAINT Evento_Gol_PK PRIMARY KEY ( id_ev_go ) ;

CREATE TABLE Evento_Partido 
    ( 
     id_ev_pa            NUMBER  NOT NULL , 
     fecha_ev_pa         DATE  NOT NULL , 
     Llave_Mundial_id_mu NUMBER  NOT NULL , 
     Llave_Mundial_id_fa NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Evento_Partido 
    ADD CONSTRAINT Evento_Partido_PK PRIMARY KEY ( id_ev_pa ) ;

CREATE TABLE Fase 
    ( 
     id_fa     NUMBER  NOT NULL , 
     nombre_fa VARCHAR2 (20)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Fase 
    ADD CONSTRAINT Fase_PK PRIMARY KEY ( id_fa ) ;

CREATE TABLE Grupo 
    ( 
     id_gr     NUMBER  NOT NULL , 
     nombre_gr CHAR (3)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Grupo 
    ADD CONSTRAINT Grupo_PK PRIMARY KEY ( id_gr ) ;

CREATE TABLE Jugador 
    ( 
     id_ju               NUMBER  NOT NULL , 
     nombre_ju           VARCHAR2 (150)  NOT NULL , 
     fecha_nacimiento_ju DATE , 
     lugar_nacimiento_ju VARCHAR2 (200) , 
     altura_ju           VARCHAR2 (5) , 
     apodo_ju            VARCHAR2 (75) , 
     pagina_web_ju       VARCHAR2 (50) 
    ) 
    LOGGING 
;

ALTER TABLE Jugador 
    ADD CONSTRAINT Jugador_PK PRIMARY KEY ( id_ju ) ;

CREATE TABLE Llave_Mundial 
    ( 
     Mundial_id_mu NUMBER  NOT NULL , 
     Fase_id_fa    NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Llave_Mundial 
    ADD CONSTRAINT Llave_Mundial_PK PRIMARY KEY ( Mundial_id_mu, Fase_id_fa ) ;

CREATE TABLE Mundial 
    ( 
     id_mu          NUMBER  NOT NULL , 
     anio_mu        NUMBER  NOT NULL , 
     organizador_mu VARCHAR2 (50)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Mundial 
    ADD CONSTRAINT Mundial_PK PRIMARY KEY ( id_mu ) ;

CREATE TABLE Pais 
    ( 
     id_pa   NUMBER  NOT NULL , 
     name_pa VARCHAR2 (70)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Pais 
    ADD CONSTRAINT Pais_PK PRIMARY KEY ( id_pa ) ;

CREATE TABLE Pais_Clasificado_Mundial 
    ( 
     Mundial_id_mu NUMBER  NOT NULL , 
     Pais_id_pa    NUMBER  NOT NULL , 
     Grupo_id_gr   NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Pais_Clasificado_Mundial 
    ADD CONSTRAINT Pais_Clasificado_Mundial_PK PRIMARY KEY ( Mundial_id_mu, Pais_id_pa, Grupo_id_gr ) ;

CREATE TABLE Partido_Plantilla 
    ( 
     Plantilla_id_pla        NUMBER  NOT NULL , 
     Evento_Partido_id_ev_pa NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Partido_Plantilla 
    ADD CONSTRAINT Partido_Plantilla_PK PRIMARY KEY ( Plantilla_id_pla, Evento_Partido_id_ev_pa ) ;

CREATE TABLE Plantilla 
    ( 
     id_pla               NUMBER  NOT NULL , 
     Pais_id_pa           NUMBER  NOT NULL , 
     director_tecnico_pla VARCHAR2 (90)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Plantilla 
    ADD CONSTRAINT Plantilla_PK PRIMARY KEY ( id_pla ) ;

CREATE TABLE Posicion_Jugador 
    ( 
     Plantilla_id_pla NUMBER  NOT NULL , 
     Jugador_id_ju    NUMBER  NOT NULL , 
     nombre_po_ju     VARCHAR2 (2) , 
     capitan          NUMBER , 
     no_camiseta      NUMBER , 
     titular          NUMBER 
    ) 
    LOGGING 
;

ALTER TABLE Posicion_Jugador 
    ADD CONSTRAINT Posicion_Jugador_PK PRIMARY KEY ( Plantilla_id_pla, Jugador_id_ju ) ;

CREATE TABLE Premio 
    ( 
     id_pre                NUMBER  NOT NULL , 
     Mundial_id_mu         NUMBER  NOT NULL , 
     pais_pre                  VARCHAR2 (90) , 
     Tipo_Premio_id_ti_pre NUMBER  NOT NULL ,
     entrenador_pre         VARCHAR2 (90)
    ) 
    LOGGING 
;

ALTER TABLE Premio 
    ADD CONSTRAINT Premio_PK PRIMARY KEY ( id_pre ) ;

CREATE TABLE Premios_Jugador 
    ( 
     Premio_id_pre NUMBER  NOT NULL , 
     Jugador_id_ju NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Premios_Jugador 
    ADD CONSTRAINT Premios_Jugador_PK PRIMARY KEY ( Premio_id_pre, Jugador_id_ju ) ;

CREATE TABLE Red_social 
    ( 
     id_red_so     NUMBER  NOT NULL , 
     nombre_red_so VARCHAR2 (50)  NOT NULL , 
     tipo_red_sp   VARCHAR2 (15)  NOT NULL , 
     Jugador_id_ju NUMBER  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Red_social 
    ADD CONSTRAINT Red_social_PK PRIMARY KEY ( id_red_so ) ;

CREATE TABLE Tipo_Premio 
    ( 
     id_ti_pre     NUMBER  NOT NULL , 
     nombre_ti_pre VARCHAR2 (90)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Tipo_Premio 
    ADD CONSTRAINT Tipo_Premio_PK PRIMARY KEY ( id_ti_pre ) ;

CREATE TABLE Tipo_Tarjeta 
    ( 
     id_ti_ta      NUMBER  NOT NULL , 
     color_tarjeta VARCHAR2 (10)  NOT NULL 
    ) 
    LOGGING 
;

ALTER TABLE Tipo_Tarjeta 
    ADD CONSTRAINT Tipo_Tarjeta_PK PRIMARY KEY ( id_ti_ta ) ;

ALTER TABLE Cambio_Jugador 
    ADD CONSTRAINT Cambio_Jugador_Evento_Cambio_Jugador_FK FOREIGN KEY 
    ( 
     Evento_Cambio_Jugador_id_ev_ca_ju
    ) 
    REFERENCES Evento_Cambio_Jugador 
    ( 
     id_ev_ca_ju
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Cambio_Jugador 
    ADD CONSTRAINT Cambio_Jugador_Jugador_FK FOREIGN KEY 
    ( 
     Jugador_id_ju
    ) 
    REFERENCES Jugador 
    ( 
     id_ju
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Evento_Cambio_Jugador 
    ADD CONSTRAINT Evento_Cambio_Jugador_Evento_Partido_FK FOREIGN KEY 
    ( 
     Evento_Partido_id_ev_pa
    ) 
    REFERENCES Evento_Partido 
    ( 
     id_ev_pa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Evento_Falta 
    ADD CONSTRAINT Evento_Falta_Evento_Partido_FK FOREIGN KEY 
    ( 
     Evento_Partido_id_ev_pa
    ) 
    REFERENCES Evento_Partido 
    ( 
     id_ev_pa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Evento_Falta 
    ADD CONSTRAINT Evento_Falta_Tipo_Tarjeta_FK FOREIGN KEY 
    ( 
     Tipo_Tarjeta_id_ti_ta
    ) 
    REFERENCES Tipo_Tarjeta 
    ( 
     id_ti_ta
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Evento_Gol 
    ADD CONSTRAINT Evento_Gol_Evento_Partido_FK FOREIGN KEY 
    ( 
     Evento_Partido_id_ev_pa
    ) 
    REFERENCES Evento_Partido 
    ( 
     id_ev_pa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Evento_Gol 
    ADD CONSTRAINT Evento_Gol_Jugador_FK FOREIGN KEY 
    ( 
     Jugador_id_ju
    ) 
    REFERENCES Jugador 
    ( 
     id_ju
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Evento_Partido 
    ADD CONSTRAINT Evento_Partido_Llave_Mundial_FK FOREIGN KEY 
    ( 
     Llave_Mundial_id_mu,
     Llave_Mundial_id_fa
    ) 
    REFERENCES Llave_Mundial 
    ( 
     Mundial_id_mu,
     Fase_id_fa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Llave_Mundial 
    ADD CONSTRAINT Llave_Mundial_Fase_FK FOREIGN KEY 
    ( 
     Fase_id_fa
    ) 
    REFERENCES Fase 
    ( 
     id_fa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Llave_Mundial 
    ADD CONSTRAINT Llave_Mundial_Mundial_FK FOREIGN KEY 
    ( 
     Mundial_id_mu
    ) 
    REFERENCES Mundial 
    ( 
     id_mu
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Pais_Clasificado_Mundial 
    ADD CONSTRAINT Pais_Clasificado_Mundial_Grupo_FK FOREIGN KEY 
    ( 
     Grupo_id_gr
    ) 
    REFERENCES Grupo 
    ( 
     id_gr
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Pais_Clasificado_Mundial 
    ADD CONSTRAINT Pais_Clasificado_Mundial_Mundial_FK FOREIGN KEY 
    ( 
     Mundial_id_mu
    ) 
    REFERENCES Mundial 
    ( 
     id_mu
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Pais_Clasificado_Mundial 
    ADD CONSTRAINT Pais_Clasificado_Mundial_Pais_FK FOREIGN KEY 
    ( 
     Pais_id_pa
    ) 
    REFERENCES Pais 
    ( 
     id_pa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Partido_Plantilla 
    ADD CONSTRAINT Partido_Plantilla_Evento_Partido_FK FOREIGN KEY 
    ( 
     Evento_Partido_id_ev_pa
    ) 
    REFERENCES Evento_Partido 
    ( 
     id_ev_pa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Partido_Plantilla 
    ADD CONSTRAINT Partido_Plantilla_Plantilla_FK FOREIGN KEY 
    ( 
     Plantilla_id_pla
    ) 
    REFERENCES Plantilla 
    ( 
     id_pla
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Plantilla 
    ADD CONSTRAINT Plantilla_Pais_FK FOREIGN KEY 
    ( 
     Pais_id_pa
    ) 
    REFERENCES Pais 
    ( 
     id_pa
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Posicion_Jugador 
    ADD CONSTRAINT Posicion_Jugador_Jugador_FK FOREIGN KEY 
    ( 
     Jugador_id_ju
    ) 
    REFERENCES Jugador 
    ( 
     id_ju
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Posicion_Jugador 
    ADD CONSTRAINT Posicion_Jugador_Plantilla_FK FOREIGN KEY 
    ( 
     Plantilla_id_pla
    ) 
    REFERENCES Plantilla 
    ( 
     id_pla
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Premio 
    ADD CONSTRAINT Premio_Mundial_FK FOREIGN KEY 
    ( 
     Mundial_id_mu
    ) 
    REFERENCES Mundial 
    ( 
     id_mu
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Premio 
    ADD CONSTRAINT Premio_Tipo_Premio_FK FOREIGN KEY 
    ( 
     Tipo_Premio_id_ti_pre
    ) 
    REFERENCES Tipo_Premio 
    ( 
     id_ti_pre
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Premios_Jugador 
    ADD CONSTRAINT Premios_Jugador_Jugador_FK FOREIGN KEY 
    ( 
     Jugador_id_ju
    ) 
    REFERENCES Jugador 
    ( 
     id_ju
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Premios_Jugador 
    ADD CONSTRAINT Premios_Jugador_Premio_FK FOREIGN KEY 
    ( 
     Premio_id_pre
    ) 
    REFERENCES Premio 
    ( 
     id_pre
    ) 
    NOT DEFERRABLE 
;

ALTER TABLE Red_social 
    ADD CONSTRAINT Red_social_Jugador_FK FOREIGN KEY 
    ( 
     Jugador_id_ju
    ) 
    REFERENCES Jugador 
    ( 
     id_ju
    ) 
    NOT DEFERRABLE 
;



-- =============================================================
-- TABLAS DE LOG (Registro / Bitacora)
-- Cada tabla LOG almacena:
--   - log_id:         Identificador unico autogenerado
--   - log_operacion:  Tipo de operacion (INSERT, UPDATE, DELETE)
--   - log_fecha:      Fecha y hora de la operacion
--   - log_usuario:    Usuario que realizo la operacion
--   - Todas las columnas de la tabla original (sin constraints)
-- =============================================================

CREATE TABLE Log_Cambio_Jugador
    (
     log_id                            NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion                     VARCHAR2 (10) NOT NULL ,
     log_fecha                         TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario                       VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ca_ju                          NUMBER ,
     Evento_Cambio_Jugador_id_ev_ca_ju NUMBER ,
     Jugador_id_ju                     NUMBER ,
     tiempo_ca_ju                      VARCHAR2 (8) ,
     CONSTRAINT Log_Cambio_Jugador_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Evento_Cambio_Jugador
    (
     log_id                  NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion           VARCHAR2 (10) NOT NULL ,
     log_fecha               TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario             VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ev_ca_ju             NUMBER ,
     Evento_Partido_id_ev_pa NUMBER ,
     CONSTRAINT Log_Evento_Cambio_Jugador_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Evento_Falta
    (
     log_id                  NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion           VARCHAR2 (10) NOT NULL ,
     log_fecha               TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario             VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ev_fa                NUMBER ,
     Evento_Partido_id_ev_pa NUMBER ,
     Tipo_Tarjeta_id_ti_ta   NUMBER ,
     minuto_falta            VARCHAR2 (8) ,
     entre_tiempo            NUMBER ,
     CONSTRAINT Log_Evento_Falta_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Evento_Gol
    (
     log_id                  NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion           VARCHAR2 (10) NOT NULL ,
     log_fecha               TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario             VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ev_go                NUMBER ,
     Evento_Partido_id_ev_pa NUMBER ,
     Jugador_id_ju           NUMBER ,
     tiempo_gol              VARCHAR2 (8) ,
     entre_tiempo_ev_go      VARCHAR2 (8) ,
     penal                   NUMBER ,
     CONSTRAINT Log_Evento_Gol_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Evento_Partido
    (
     log_id              NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion       VARCHAR2 (10) NOT NULL ,
     log_fecha           TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario         VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ev_pa            NUMBER ,
     fecha_ev_pa         DATE ,
     Llave_Mundial_id_mu NUMBER ,
     Llave_Mundial_id_fa NUMBER ,
     CONSTRAINT Log_Evento_Partido_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Fase
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_fa         NUMBER ,
     nombre_fa     VARCHAR2 (20) ,
     CONSTRAINT Log_Fase_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Grupo
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_gr         NUMBER ,
     nombre_gr     CHAR (3) ,
     CONSTRAINT Log_Grupo_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Jugador
    (
     log_id              NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion       VARCHAR2 (10) NOT NULL ,
     log_fecha           TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario         VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ju               NUMBER ,
     nombre_ju           VARCHAR2 (150) ,
     fecha_nacimiento_ju DATE ,
     lugar_nacimiento_ju VARCHAR2 (200) ,
     altura_ju           VARCHAR2 (5) ,
     apodo_ju            VARCHAR2 (75) ,
     pagina_web_ju       VARCHAR2 (50) ,
     CONSTRAINT Log_Jugador_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Llave_Mundial
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     Mundial_id_mu NUMBER ,
     Fase_id_fa    NUMBER ,
     CONSTRAINT Log_Llave_Mundial_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Mundial
    (
     log_id         NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion  VARCHAR2 (10) NOT NULL ,
     log_fecha      TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario    VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_mu          NUMBER ,
     anio_mu        NUMBER ,
     organizador_mu VARCHAR2 (50) ,
     CONSTRAINT Log_Mundial_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Pais
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_pa         NUMBER ,
     name_pa       VARCHAR2 (70) ,
     CONSTRAINT Log_Pais_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Pais_Clasificado_Mundial
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     Mundial_id_mu NUMBER ,
     Pais_id_pa    NUMBER ,
     Grupo_id_gr   NUMBER ,
     CONSTRAINT Log_Pais_Clas_Mundial_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Partido_Plantilla
    (
     log_id                  NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion           VARCHAR2 (10) NOT NULL ,
     log_fecha               TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario             VARCHAR2 (50) DEFAULT USER NOT NULL ,
     Plantilla_id_pla        NUMBER ,
     Evento_Partido_id_ev_pa NUMBER ,
     CONSTRAINT Log_Partido_Plantilla_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Plantilla
    (
     log_id               NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion        VARCHAR2 (10) NOT NULL ,
     log_fecha            TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario          VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_pla               NUMBER ,
     Pais_id_pa           NUMBER ,
     director_tecnico_pla VARCHAR2 (90) ,
     CONSTRAINT Log_Plantilla_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Posicion_Jugador
    (
     log_id           NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion    VARCHAR2 (10) NOT NULL ,
     log_fecha        TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario      VARCHAR2 (50) DEFAULT USER NOT NULL ,
     Plantilla_id_pla NUMBER ,
     Jugador_id_ju    NUMBER ,
     nombre_po_ju     VARCHAR2 (2) ,
     capitan          NUMBER ,
     no_camiseta      NUMBER ,
     titular          NUMBER ,
     CONSTRAINT Log_Posicion_Jugador_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Premio
    (
     log_id                NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion         VARCHAR2 (10) NOT NULL ,
     log_fecha             TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario           VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_pre                NUMBER ,
     Mundial_id_mu         NUMBER ,
     pais_pre              VARCHAR2 (90) ,
     Tipo_Premio_id_ti_pre NUMBER ,
     entrenador_pre        VARCHAR2 (90) ,
     CONSTRAINT Log_Premio_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Premios_Jugador
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     Premio_id_pre NUMBER ,
     Jugador_id_ju NUMBER ,
     CONSTRAINT Log_Premios_Jugador_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Red_social
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_red_so     NUMBER ,
     nombre_red_so VARCHAR2 (50) ,
     tipo_red_sp   VARCHAR2 (15) ,
     Jugador_id_ju NUMBER ,
     CONSTRAINT Log_Red_social_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Tipo_Premio
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ti_pre     NUMBER ,
     nombre_ti_pre VARCHAR2 (90) ,
     CONSTRAINT Log_Tipo_Premio_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

CREATE TABLE Log_Tipo_Tarjeta
    (
     log_id        NUMBER GENERATED ALWAYS AS IDENTITY ,
     log_operacion VARCHAR2 (10) NOT NULL ,
     log_fecha     TIMESTAMP DEFAULT SYSTIMESTAMP NOT NULL ,
     log_usuario   VARCHAR2 (50) DEFAULT USER NOT NULL ,
     id_ti_ta      NUMBER ,
     color_tarjeta VARCHAR2 (10) ,
     CONSTRAINT Log_Tipo_Tarjeta_PK PRIMARY KEY ( log_id )
    )
    LOGGING
;

-- =============================================================
-- TRIGGERS DE LOG
-- Cada trigger captura INSERT, UPDATE y DELETE sobre la tabla
-- original e inserta un registro en la tabla Log_ correspondiente.
-- =============================================================

CREATE OR REPLACE TRIGGER trg_log_Cambio_Jugador
AFTER INSERT OR UPDATE OR DELETE ON Cambio_Jugador
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Cambio_Jugador (log_operacion, id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju)
        VALUES (v_operacion, :NEW.id_ca_ju, :NEW.Evento_Cambio_Jugador_id_ev_ca_ju, :NEW.Jugador_id_ju, :NEW.tiempo_ca_ju);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Cambio_Jugador (log_operacion, id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju)
        VALUES (v_operacion, :NEW.id_ca_ju, :NEW.Evento_Cambio_Jugador_id_ev_ca_ju, :NEW.Jugador_id_ju, :NEW.tiempo_ca_ju);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Cambio_Jugador (log_operacion, id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju)
        VALUES (v_operacion, :OLD.id_ca_ju, :OLD.Evento_Cambio_Jugador_id_ev_ca_ju, :OLD.Jugador_id_ju, :OLD.tiempo_ca_ju);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Evento_Cambio_Jugador
AFTER INSERT OR UPDATE OR DELETE ON Evento_Cambio_Jugador
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Evento_Cambio_Jugador (log_operacion, id_ev_ca_ju, Evento_Partido_id_ev_pa)
        VALUES (v_operacion, :NEW.id_ev_ca_ju, :NEW.Evento_Partido_id_ev_pa);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Evento_Cambio_Jugador (log_operacion, id_ev_ca_ju, Evento_Partido_id_ev_pa)
        VALUES (v_operacion, :NEW.id_ev_ca_ju, :NEW.Evento_Partido_id_ev_pa);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Evento_Cambio_Jugador (log_operacion, id_ev_ca_ju, Evento_Partido_id_ev_pa)
        VALUES (v_operacion, :OLD.id_ev_ca_ju, :OLD.Evento_Partido_id_ev_pa);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Evento_Falta
AFTER INSERT OR UPDATE OR DELETE ON Evento_Falta
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Evento_Falta (log_operacion, id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo)
        VALUES (v_operacion, :NEW.id_ev_fa, :NEW.Evento_Partido_id_ev_pa, :NEW.Tipo_Tarjeta_id_ti_ta, :NEW.minuto_falta, :NEW.entre_tiempo);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Evento_Falta (log_operacion, id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo)
        VALUES (v_operacion, :NEW.id_ev_fa, :NEW.Evento_Partido_id_ev_pa, :NEW.Tipo_Tarjeta_id_ti_ta, :NEW.minuto_falta, :NEW.entre_tiempo);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Evento_Falta (log_operacion, id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo)
        VALUES (v_operacion, :OLD.id_ev_fa, :OLD.Evento_Partido_id_ev_pa, :OLD.Tipo_Tarjeta_id_ti_ta, :OLD.minuto_falta, :OLD.entre_tiempo);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Evento_Gol
AFTER INSERT OR UPDATE OR DELETE ON Evento_Gol
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Evento_Gol (log_operacion, id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal)
        VALUES (v_operacion, :NEW.id_ev_go, :NEW.Evento_Partido_id_ev_pa, :NEW.Jugador_id_ju, :NEW.tiempo_gol, :NEW.entre_tiempo_ev_go, :NEW.penal);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Evento_Gol (log_operacion, id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal)
        VALUES (v_operacion, :NEW.id_ev_go, :NEW.Evento_Partido_id_ev_pa, :NEW.Jugador_id_ju, :NEW.tiempo_gol, :NEW.entre_tiempo_ev_go, :NEW.penal);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Evento_Gol (log_operacion, id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal)
        VALUES (v_operacion, :OLD.id_ev_go, :OLD.Evento_Partido_id_ev_pa, :OLD.Jugador_id_ju, :OLD.tiempo_gol, :OLD.entre_tiempo_ev_go, :OLD.penal);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Evento_Partido
AFTER INSERT OR UPDATE OR DELETE ON Evento_Partido
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Evento_Partido (log_operacion, id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa)
        VALUES (v_operacion, :NEW.id_ev_pa, :NEW.fecha_ev_pa, :NEW.Llave_Mundial_id_mu, :NEW.Llave_Mundial_id_fa);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Evento_Partido (log_operacion, id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa)
        VALUES (v_operacion, :NEW.id_ev_pa, :NEW.fecha_ev_pa, :NEW.Llave_Mundial_id_mu, :NEW.Llave_Mundial_id_fa);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Evento_Partido (log_operacion, id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa)
        VALUES (v_operacion, :OLD.id_ev_pa, :OLD.fecha_ev_pa, :OLD.Llave_Mundial_id_mu, :OLD.Llave_Mundial_id_fa);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Fase
AFTER INSERT OR UPDATE OR DELETE ON Fase
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Fase (log_operacion, id_fa, nombre_fa)
        VALUES (v_operacion, :NEW.id_fa, :NEW.nombre_fa);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Fase (log_operacion, id_fa, nombre_fa)
        VALUES (v_operacion, :NEW.id_fa, :NEW.nombre_fa);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Fase (log_operacion, id_fa, nombre_fa)
        VALUES (v_operacion, :OLD.id_fa, :OLD.nombre_fa);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Grupo
AFTER INSERT OR UPDATE OR DELETE ON Grupo
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Grupo (log_operacion, id_gr, nombre_gr)
        VALUES (v_operacion, :NEW.id_gr, :NEW.nombre_gr);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Grupo (log_operacion, id_gr, nombre_gr)
        VALUES (v_operacion, :NEW.id_gr, :NEW.nombre_gr);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Grupo (log_operacion, id_gr, nombre_gr)
        VALUES (v_operacion, :OLD.id_gr, :OLD.nombre_gr);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Jugador
AFTER INSERT OR UPDATE OR DELETE ON Jugador
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Jugador (log_operacion, id_ju, nombre_ju, fecha_nacimiento_ju, lugar_nacimiento_ju, altura_ju, apodo_ju, pagina_web_ju)
        VALUES (v_operacion, :NEW.id_ju, :NEW.nombre_ju, :NEW.fecha_nacimiento_ju, :NEW.lugar_nacimiento_ju, :NEW.altura_ju, :NEW.apodo_ju, :NEW.pagina_web_ju);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Jugador (log_operacion, id_ju, nombre_ju, fecha_nacimiento_ju, lugar_nacimiento_ju, altura_ju, apodo_ju, pagina_web_ju)
        VALUES (v_operacion, :NEW.id_ju, :NEW.nombre_ju, :NEW.fecha_nacimiento_ju, :NEW.lugar_nacimiento_ju, :NEW.altura_ju, :NEW.apodo_ju, :NEW.pagina_web_ju);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Jugador (log_operacion, id_ju, nombre_ju, fecha_nacimiento_ju, lugar_nacimiento_ju, altura_ju, apodo_ju, pagina_web_ju)
        VALUES (v_operacion, :OLD.id_ju, :OLD.nombre_ju, :OLD.fecha_nacimiento_ju, :OLD.lugar_nacimiento_ju, :OLD.altura_ju, :OLD.apodo_ju, :OLD.pagina_web_ju);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Llave_Mundial
AFTER INSERT OR UPDATE OR DELETE ON Llave_Mundial
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Llave_Mundial (log_operacion, Mundial_id_mu, Fase_id_fa)
        VALUES (v_operacion, :NEW.Mundial_id_mu, :NEW.Fase_id_fa);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Llave_Mundial (log_operacion, Mundial_id_mu, Fase_id_fa)
        VALUES (v_operacion, :NEW.Mundial_id_mu, :NEW.Fase_id_fa);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Llave_Mundial (log_operacion, Mundial_id_mu, Fase_id_fa)
        VALUES (v_operacion, :OLD.Mundial_id_mu, :OLD.Fase_id_fa);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Mundial
AFTER INSERT OR UPDATE OR DELETE ON Mundial
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Mundial (log_operacion, id_mu, anio_mu, organizador_mu)
        VALUES (v_operacion, :NEW.id_mu, :NEW.anio_mu, :NEW.organizador_mu);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Mundial (log_operacion, id_mu, anio_mu, organizador_mu)
        VALUES (v_operacion, :NEW.id_mu, :NEW.anio_mu, :NEW.organizador_mu);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Mundial (log_operacion, id_mu, anio_mu, organizador_mu)
        VALUES (v_operacion, :OLD.id_mu, :OLD.anio_mu, :OLD.organizador_mu);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Pais
AFTER INSERT OR UPDATE OR DELETE ON Pais
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Pais (log_operacion, id_pa, name_pa)
        VALUES (v_operacion, :NEW.id_pa, :NEW.name_pa);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Pais (log_operacion, id_pa, name_pa)
        VALUES (v_operacion, :NEW.id_pa, :NEW.name_pa);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Pais (log_operacion, id_pa, name_pa)
        VALUES (v_operacion, :OLD.id_pa, :OLD.name_pa);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Pais_Clas_Mundial
AFTER INSERT OR UPDATE OR DELETE ON Pais_Clasificado_Mundial
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Pais_Clasificado_Mundial (log_operacion, Mundial_id_mu, Pais_id_pa, Grupo_id_gr)
        VALUES (v_operacion, :NEW.Mundial_id_mu, :NEW.Pais_id_pa, :NEW.Grupo_id_gr);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Pais_Clasificado_Mundial (log_operacion, Mundial_id_mu, Pais_id_pa, Grupo_id_gr)
        VALUES (v_operacion, :NEW.Mundial_id_mu, :NEW.Pais_id_pa, :NEW.Grupo_id_gr);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Pais_Clasificado_Mundial (log_operacion, Mundial_id_mu, Pais_id_pa, Grupo_id_gr)
        VALUES (v_operacion, :OLD.Mundial_id_mu, :OLD.Pais_id_pa, :OLD.Grupo_id_gr);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Partido_Plantilla
AFTER INSERT OR UPDATE OR DELETE ON Partido_Plantilla
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Partido_Plantilla (log_operacion, Plantilla_id_pla, Evento_Partido_id_ev_pa)
        VALUES (v_operacion, :NEW.Plantilla_id_pla, :NEW.Evento_Partido_id_ev_pa);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Partido_Plantilla (log_operacion, Plantilla_id_pla, Evento_Partido_id_ev_pa)
        VALUES (v_operacion, :NEW.Plantilla_id_pla, :NEW.Evento_Partido_id_ev_pa);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Partido_Plantilla (log_operacion, Plantilla_id_pla, Evento_Partido_id_ev_pa)
        VALUES (v_operacion, :OLD.Plantilla_id_pla, :OLD.Evento_Partido_id_ev_pa);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Plantilla
AFTER INSERT OR UPDATE OR DELETE ON Plantilla
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Plantilla (log_operacion, id_pla, Pais_id_pa, director_tecnico_pla)
        VALUES (v_operacion, :NEW.id_pla, :NEW.Pais_id_pa, :NEW.director_tecnico_pla);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Plantilla (log_operacion, id_pla, Pais_id_pa, director_tecnico_pla)
        VALUES (v_operacion, :NEW.id_pla, :NEW.Pais_id_pa, :NEW.director_tecnico_pla);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Plantilla (log_operacion, id_pla, Pais_id_pa, director_tecnico_pla)
        VALUES (v_operacion, :OLD.id_pla, :OLD.Pais_id_pa, :OLD.director_tecnico_pla);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Posicion_Jugador
AFTER INSERT OR UPDATE OR DELETE ON Posicion_Jugador
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Posicion_Jugador (log_operacion, Plantilla_id_pla, Jugador_id_ju, nombre_po_ju, capitan, no_camiseta, titular)
        VALUES (v_operacion, :NEW.Plantilla_id_pla, :NEW.Jugador_id_ju, :NEW.nombre_po_ju, :NEW.capitan, :NEW.no_camiseta, :NEW.titular);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Posicion_Jugador (log_operacion, Plantilla_id_pla, Jugador_id_ju, nombre_po_ju, capitan, no_camiseta, titular)
        VALUES (v_operacion, :NEW.Plantilla_id_pla, :NEW.Jugador_id_ju, :NEW.nombre_po_ju, :NEW.capitan, :NEW.no_camiseta, :NEW.titular);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Posicion_Jugador (log_operacion, Plantilla_id_pla, Jugador_id_ju, nombre_po_ju, capitan, no_camiseta, titular)
        VALUES (v_operacion, :OLD.Plantilla_id_pla, :OLD.Jugador_id_ju, :OLD.nombre_po_ju, :OLD.capitan, :OLD.no_camiseta, :OLD.titular);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Premio
AFTER INSERT OR UPDATE OR DELETE ON Premio
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Premio (log_operacion, id_pre, Mundial_id_mu, pais_pre, Tipo_Premio_id_ti_pre, entrenador_pre)
        VALUES (v_operacion, :NEW.id_pre, :NEW.Mundial_id_mu, :NEW.pais_pre, :NEW.Tipo_Premio_id_ti_pre, :NEW.entrenador_pre);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Premio (log_operacion, id_pre, Mundial_id_mu, pais_pre, Tipo_Premio_id_ti_pre, entrenador_pre)
        VALUES (v_operacion, :NEW.id_pre, :NEW.Mundial_id_mu, :NEW.pais_pre, :NEW.Tipo_Premio_id_ti_pre, :NEW.entrenador_pre);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Premio (log_operacion, id_pre, Mundial_id_mu, pais_pre, Tipo_Premio_id_ti_pre, entrenador_pre)
        VALUES (v_operacion, :OLD.id_pre, :OLD.Mundial_id_mu, :OLD.pais_pre, :OLD.Tipo_Premio_id_ti_pre, :OLD.entrenador_pre);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Premios_Jugador
AFTER INSERT OR UPDATE OR DELETE ON Premios_Jugador
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Premios_Jugador (log_operacion, Premio_id_pre, Jugador_id_ju)
        VALUES (v_operacion, :NEW.Premio_id_pre, :NEW.Jugador_id_ju);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Premios_Jugador (log_operacion, Premio_id_pre, Jugador_id_ju)
        VALUES (v_operacion, :NEW.Premio_id_pre, :NEW.Jugador_id_ju);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Premios_Jugador (log_operacion, Premio_id_pre, Jugador_id_ju)
        VALUES (v_operacion, :OLD.Premio_id_pre, :OLD.Jugador_id_ju);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Red_social
AFTER INSERT OR UPDATE OR DELETE ON Red_social
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Red_social (log_operacion, id_red_so, nombre_red_so, tipo_red_sp, Jugador_id_ju)
        VALUES (v_operacion, :NEW.id_red_so, :NEW.nombre_red_so, :NEW.tipo_red_sp, :NEW.Jugador_id_ju);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Red_social (log_operacion, id_red_so, nombre_red_so, tipo_red_sp, Jugador_id_ju)
        VALUES (v_operacion, :NEW.id_red_so, :NEW.nombre_red_so, :NEW.tipo_red_sp, :NEW.Jugador_id_ju);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Red_social (log_operacion, id_red_so, nombre_red_so, tipo_red_sp, Jugador_id_ju)
        VALUES (v_operacion, :OLD.id_red_so, :OLD.nombre_red_so, :OLD.tipo_red_sp, :OLD.Jugador_id_ju);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Tipo_Premio
AFTER INSERT OR UPDATE OR DELETE ON Tipo_Premio
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Tipo_Premio (log_operacion, id_ti_pre, nombre_ti_pre)
        VALUES (v_operacion, :NEW.id_ti_pre, :NEW.nombre_ti_pre);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Tipo_Premio (log_operacion, id_ti_pre, nombre_ti_pre)
        VALUES (v_operacion, :NEW.id_ti_pre, :NEW.nombre_ti_pre);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Tipo_Premio (log_operacion, id_ti_pre, nombre_ti_pre)
        VALUES (v_operacion, :OLD.id_ti_pre, :OLD.nombre_ti_pre);
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_log_Tipo_Tarjeta
AFTER INSERT OR UPDATE OR DELETE ON Tipo_Tarjeta
FOR EACH ROW
DECLARE
    v_operacion VARCHAR2(10);
BEGIN
    IF INSERTING THEN
        v_operacion := 'INSERT';
        INSERT INTO Log_Tipo_Tarjeta (log_operacion, id_ti_ta, color_tarjeta)
        VALUES (v_operacion, :NEW.id_ti_ta, :NEW.color_tarjeta);
    ELSIF UPDATING THEN
        v_operacion := 'UPDATE';
        INSERT INTO Log_Tipo_Tarjeta (log_operacion, id_ti_ta, color_tarjeta)
        VALUES (v_operacion, :NEW.id_ti_ta, :NEW.color_tarjeta);
    ELSIF DELETING THEN
        v_operacion := 'DELETE';
        INSERT INTO Log_Tipo_Tarjeta (log_operacion, id_ti_ta, color_tarjeta)
        VALUES (v_operacion, :OLD.id_ti_ta, :OLD.color_tarjeta);
    END IF;
END;
/
