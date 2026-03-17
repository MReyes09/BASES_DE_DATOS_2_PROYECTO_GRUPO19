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
     entrenador_pre         VARCHAR2 (90);
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



-- Informe de Resumen de Oracle SQL Developer Data Modeler: 
-- 
-- CREATE TABLE                            20
-- CREATE INDEX                             0
-- ALTER TABLE                             43
-- CREATE VIEW                              0
-- ALTER VIEW                               0
-- CREATE PACKAGE                           0
-- CREATE PACKAGE BODY                      0
-- CREATE PROCEDURE                         0
-- CREATE FUNCTION                          0
-- CREATE TRIGGER                           0
-- ALTER TRIGGER                            0
-- CREATE COLLECTION TYPE                   0
-- CREATE STRUCTURED TYPE                   0
-- CREATE STRUCTURED TYPE BODY              0
-- CREATE CLUSTER                           0
-- CREATE CONTEXT                           0
-- CREATE DATABASE                          0
-- CREATE DIMENSION                         0
-- CREATE DIRECTORY                         0
-- CREATE DISK GROUP                        0
-- CREATE ROLE                              0
-- CREATE ROLLBACK SEGMENT                  0
-- CREATE SEQUENCE                          0
-- CREATE MATERIALIZED VIEW                 0
-- CREATE MATERIALIZED VIEW LOG             0
-- CREATE SYNONYM                           0
-- CREATE TABLESPACE                        0
-- CREATE USER                              0
-- 
-- DROP TABLESPACE                          0
-- DROP DATABASE                            0
-- 
-- REDACTION POLICY                         0
-- 
-- ORDS DROP SCHEMA                         0
-- ORDS ENABLE SCHEMA                       0
-- ORDS ENABLE OBJECT                       0
-- 
-- ERRORS                                   0
-- WARNINGS                                 0
