-- ============================================================
-- SCRIPT: DROP ALL TABLES - Proyecto Mundiales de Fútbol
-- Oracle Database 21c
-- Orden: tablas hijas primero, luego tablas padre
-- ============================================================

-- Nivel 1: Tablas con más dependencias (hijas directas)
DROP TABLE Cambio_Jugador        CASCADE CONSTRAINTS;
DROP TABLE Evento_Falta          CASCADE CONSTRAINTS;
DROP TABLE Evento_Gol            CASCADE CONSTRAINTS;
DROP TABLE Partido_Plantilla     CASCADE CONSTRAINTS;
DROP TABLE Posicion_Jugador      CASCADE CONSTRAINTS;
DROP TABLE Premios_Jugador       CASCADE CONSTRAINTS;
DROP TABLE Red_social            CASCADE CONSTRAINTS;

-- Nivel 2: Tablas intermedias
DROP TABLE Evento_Cambio_Jugador CASCADE CONSTRAINTS;
DROP TABLE Evento_Partido        CASCADE CONSTRAINTS;
DROP TABLE Premio                CASCADE CONSTRAINTS;
DROP TABLE Plantilla             CASCADE CONSTRAINTS;

-- Nivel 3: Tablas de catálogo / puente
DROP TABLE Llave_Mundial         CASCADE CONSTRAINTS;
DROP TABLE Pais_Clasificado_Mundial CASCADE CONSTRAINTS;

-- Nivel 4: Tablas maestro / independientes
DROP TABLE Jugador               CASCADE CONSTRAINTS;
DROP TABLE Mundial               CASCADE CONSTRAINTS;
DROP TABLE Pais                  CASCADE CONSTRAINTS;
DROP TABLE Fase                  CASCADE CONSTRAINTS;
DROP TABLE Grupo                 CASCADE CONSTRAINTS;
DROP TABLE Tipo_Premio           CASCADE CONSTRAINTS;
DROP TABLE Tipo_Tarjeta          CASCADE CONSTRAINTS;