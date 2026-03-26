-- =============================================================
-- SELECT COUNT(*) de cada tabla
-- Oracle Database 21c
-- =============================================================

-- ===================== TABLAS ORIGINALES =====================

SELECT 'Cambio_Jugador' AS tabla, COUNT(*) AS total FROM Cambio_Jugador;
SELECT 'Evento_Cambio_Jugador' AS tabla, COUNT(*) AS total FROM Evento_Cambio_Jugador;
SELECT 'Evento_Falta' AS tabla, COUNT(*) AS total FROM Evento_Falta;
SELECT 'Evento_Gol' AS tabla, COUNT(*) AS total FROM Evento_Gol;
SELECT 'Evento_Partido' AS tabla, COUNT(*) AS total FROM Evento_Partido;
SELECT 'Fase' AS tabla, COUNT(*) AS total FROM Fase;
SELECT 'Grupo' AS tabla, COUNT(*) AS total FROM Grupo;
SELECT 'Jugador' AS tabla, COUNT(*) AS total FROM Jugador;
SELECT 'Llave_Mundial' AS tabla, COUNT(*) AS total FROM Llave_Mundial;
SELECT 'Mundial' AS tabla, COUNT(*) AS total FROM Mundial;
SELECT 'Pais' AS tabla, COUNT(*) AS total FROM Pais;
SELECT 'Pais_Clasificado_Mundial' AS tabla, COUNT(*) AS total FROM Pais_Clasificado_Mundial;
SELECT 'Partido_Plantilla' AS tabla, COUNT(*) AS total FROM Partido_Plantilla;
SELECT 'Plantilla' AS tabla, COUNT(*) AS total FROM Plantilla;
SELECT 'Posicion_Jugador' AS tabla, COUNT(*) AS total FROM Posicion_Jugador;
SELECT 'Premio' AS tabla, COUNT(*) AS total FROM Premio;
SELECT 'Premios_Jugador' AS tabla, COUNT(*) AS total FROM Premios_Jugador;
SELECT 'Red_social' AS tabla, COUNT(*) AS total FROM Red_social;
SELECT 'Tipo_Premio' AS tabla, COUNT(*) AS total FROM Tipo_Premio;
SELECT 'Tipo_Tarjeta' AS tabla, COUNT(*) AS total FROM Tipo_Tarjeta;

-- ===================== TABLAS DE LOG =====================

SELECT 'Log_Cambio_Jugador' AS tabla, COUNT(*) AS total FROM Log_Cambio_Jugador;
SELECT 'Log_Evento_Cambio_Jugador' AS tabla, COUNT(*) AS total FROM Log_Evento_Cambio_Jugador;
SELECT 'Log_Evento_Falta' AS tabla, COUNT(*) AS total FROM Log_Evento_Falta;
SELECT 'Log_Evento_Gol' AS tabla, COUNT(*) AS total FROM Log_Evento_Gol;
SELECT 'Log_Evento_Partido' AS tabla, COUNT(*) AS total FROM Log_Evento_Partido;
SELECT 'Log_Fase' AS tabla, COUNT(*) AS total FROM Log_Fase;
SELECT 'Log_Grupo' AS tabla, COUNT(*) AS total FROM Log_Grupo;
SELECT 'Log_Jugador' AS tabla, COUNT(*) AS total FROM Log_Jugador;
SELECT 'Log_Llave_Mundial' AS tabla, COUNT(*) AS total FROM Log_Llave_Mundial;
SELECT 'Log_Mundial' AS tabla, COUNT(*) AS total FROM Log_Mundial;
SELECT 'Log_Pais' AS tabla, COUNT(*) AS total FROM Log_Pais;
SELECT 'Log_Pais_Clasificado_Mundial' AS tabla, COUNT(*) AS total FROM Log_Pais_Clasificado_Mundial;
SELECT 'Log_Partido_Plantilla' AS tabla, COUNT(*) AS total FROM Log_Partido_Plantilla;
SELECT 'Log_Plantilla' AS tabla, COUNT(*) AS total FROM Log_Plantilla;
SELECT 'Log_Posicion_Jugador' AS tabla, COUNT(*) AS total FROM Log_Posicion_Jugador;
SELECT 'Log_Premio' AS tabla, COUNT(*) AS total FROM Log_Premio;
SELECT 'Log_Premios_Jugador' AS tabla, COUNT(*) AS total FROM Log_Premios_Jugador;
SELECT 'Log_Red_social' AS tabla, COUNT(*) AS total FROM Log_Red_social;
SELECT 'Log_Tipo_Premio' AS tabla, COUNT(*) AS total FROM Log_Tipo_Premio;
SELECT 'Log_Tipo_Tarjeta' AS tabla, COUNT(*) AS total FROM Log_Tipo_Tarjeta;
