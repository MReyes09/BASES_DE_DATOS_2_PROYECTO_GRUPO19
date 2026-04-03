-- =============================================================
-- Script para eliminar TODAS las tablas y triggers del DDL Fase 2
-- Orden: Triggers -> Tablas hijas (LOG + originales) -> Tablas padre
-- Oracle Database 21c
-- =============================================================

-- 1. DROP TRIGGERS
DROP TRIGGER trg_log_Cambio_Jugador;
DROP TRIGGER trg_log_Evento_Cambio_Jugador;
DROP TRIGGER trg_log_Evento_Falta;
DROP TRIGGER trg_log_Evento_Gol;
DROP TRIGGER trg_log_Evento_Partido;
DROP TRIGGER trg_log_Fase;
DROP TRIGGER trg_log_Grupo;
DROP TRIGGER trg_log_Jugador;
DROP TRIGGER trg_log_Llave_Mundial;
DROP TRIGGER trg_log_Mundial;
DROP TRIGGER trg_log_Pais;
DROP TRIGGER trg_log_Pais_Clas_Mundial;
DROP TRIGGER trg_log_Partido_Plantilla;
DROP TRIGGER trg_log_Plantilla;
DROP TRIGGER trg_log_Posicion_Jugador;
DROP TRIGGER trg_log_Premio;
DROP TRIGGER trg_log_Premios_Jugador;
DROP TRIGGER trg_log_Red_social;
DROP TRIGGER trg_log_Tipo_Premio;
DROP TRIGGER trg_log_Tipo_Tarjeta;

-- 2. DROP TABLAS DE LOG (sin dependencias entre ellas)
DROP TABLE Log_Cambio_Jugador;
DROP TABLE Log_Evento_Cambio_Jugador;
DROP TABLE Log_Evento_Falta;
DROP TABLE Log_Evento_Gol;
DROP TABLE Log_Evento_Partido;
DROP TABLE Log_Fase;
DROP TABLE Log_Grupo;
DROP TABLE Log_Jugador;
DROP TABLE Log_Llave_Mundial;
DROP TABLE Log_Mundial;
DROP TABLE Log_Pais;
DROP TABLE Log_Pais_Clasificado_Mundial;
DROP TABLE Log_Partido_Plantilla;
DROP TABLE Log_Plantilla;
DROP TABLE Log_Posicion_Jugador;
DROP TABLE Log_Premio;
DROP TABLE Log_Premios_Jugador;
DROP TABLE Log_Red_social;
DROP TABLE Log_Tipo_Premio;
DROP TABLE Log_Tipo_Tarjeta;

-- 3. DROP TABLAS ORIGINALES (hijas primero, padres despues)
DROP TABLE Cambio_Jugador;
DROP TABLE Evento_Cambio_Jugador;
DROP TABLE Evento_Falta;
DROP TABLE Evento_Gol;
DROP TABLE Posicion_Jugador;
DROP TABLE Premios_Jugador;
DROP TABLE Red_social;
DROP TABLE Partido_Plantilla;
DROP TABLE Premio;
DROP TABLE Evento_Partido;
DROP TABLE Pais_Clasificado_Mundial;
DROP TABLE Llave_Mundial;
DROP TABLE Plantilla;
DROP TABLE Jugador;
DROP TABLE Pais;
DROP TABLE Mundial;
DROP TABLE Fase;
DROP TABLE Grupo;
DROP TABLE Tipo_Premio;
DROP TABLE Tipo_Tarjeta;
