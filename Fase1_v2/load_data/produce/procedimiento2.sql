CREATE OR REPLACE PROCEDURE Consultar_Historial_Pais (
    p_nombre_pais IN VARCHAR2,
    p_anio_filtro IN NUMBER DEFAULT NULL -- Parámetro opcional para filtrar un año específico
) AS
    v_id_pais NUMBER;
    v_es_sede NUMBER;

    -- Cursor para obtener las participaciones del país en los mundiales
    CURSOR c_participaciones IS
        SELECT m.anio_mu, m.organizador_mu, g.nombre_gr, p_pla.id_pla
        FROM Pais p
        JOIN Pais_Clasificado_Mundial pcm ON p.id_pa = pcm.Pais_id_pa
        JOIN Mundial m ON pcm.Mundial_id_mu = m.id_mu
        JOIN Grupo g ON pcm.Grupo_id_gr = g.id_gr
        JOIN Plantilla p_pla ON p.id_pa = p_pla.Pais_id_pa
        WHERE p.name_pa = p_nombre_pais
          AND (p_anio_filtro IS NULL OR m.anio_mu = p_anio_filtro);

BEGIN
    -- 1. Validar existencia del país y obtener ID
    SELECT id_pa INTO v_id_pais FROM Pais WHERE name_pa = p_nombre_pais;

    DBMS_OUTPUT.PUT_LINE('====================================================');
    DBMS_OUTPUT.PUT_LINE('INFORME HISTÓRICO: ' || UPPER(p_nombre_pais));
    DBMS_OUTPUT.PUT_LINE('====================================================');

    -- 2. Verificar si ha sido sede
    DBMS_OUTPUT.PUT_LINE('¿HA SIDO SEDE?');
    FOR r_sede IN (SELECT anio_mu FROM Mundial WHERE organizador_mu = p_nombre_pais) LOOP
        DBMS_OUTPUT.PUT_LINE('- Sí, en el año: ' || r_sede.anio_mu);
        v_es_sede := 1;
    END LOOP;
    
    IF v_es_sede IS NULL THEN
        DBMS_OUTPUT.PUT_LINE('- No ha sido organizador registrado.');
    END IF;

    DBMS_OUTPUT.PUT_LINE(CHR(10) || 'DETALLE DE PARTICIPACIONES:');
    
    -- 3. Iterar por cada Mundial en el que participó
    FOR r_part IN c_participaciones LOOP
        DBMS_OUTPUT.PUT_LINE('----------------------------------------------------');
        DBMS_OUTPUT.PUT_LINE('AÑO: ' || r_part.anio_mu || ' | GRUPO: ' || r_part.nombre_gr);
        DBMS_OUTPUT.PUT_LINE('Sede del torneo: ' || r_part.organizador_mu);
        
        -- 4. Consultar partidos de esa participación (usando la tabla Partido_Plantilla)
        DBMS_OUTPUT.PUT_LINE('PARTIDOS DISPUTADOS:');
        
        FOR r_partido IN (
            SELECT ep.id_ev_pa, ep.fecha_ev_pa, f.nombre_fa
            FROM Evento_Partido ep
            JOIN Partido_Plantilla pp ON ep.id_ev_pa = pp.Evento_Partido_id_ev_pa
            JOIN Fase f ON ep.Llave_Mundial_id_fa = f.id_fa
            WHERE pp.Plantilla_id_pla = r_part.id_pla
        ) LOOP
            -- Calcular goles a favor (conteo simple de la tabla Evento_Gol)
            DECLARE
                v_goles_favor NUMBER;
            BEGIN
                SELECT COUNT(*) INTO v_goles_favor 
                FROM Evento_Gol 
                WHERE Evento_Partido_id_ev_pa = r_partido.id_ev_pa
                  AND Jugador_id_ju IN (SELECT Jugador_id_ju FROM Posicion_Jugador WHERE Plantilla_id_pla = r_part.id_pla);
                
                DBMS_OUTPUT.PUT_LINE('  > Fecha: ' || TO_CHAR(r_partido.fecha_ev_pa, 'DD/MM/YYYY') || 
                                     ' | Fase: ' || r_partido.nombre_fa || 
                                     ' | Goles anotados por el país: ' || v_goles_favor);
            END;
        END LOOP;
    END LOOP;

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Error: El país "' || p_nombre_pais || '" no se encuentra en la base de datos.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('Error inesperado: ' || SQLERRM);
END;
/

SET SERVEROUTPUT ON;

-- Consultar toda la historia de un país
EXEC Consultar_Historial_Pais('Brasil');