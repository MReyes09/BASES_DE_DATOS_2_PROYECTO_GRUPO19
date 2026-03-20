-- ============================================================================
-- STORED PROCEDURE: SP_INFO_MUNDIAL
-- Descripción: Muestra toda la información relacionada con un mundial específico
-- Parámetros:
--   p_anio_mundial (OBLIGATORIO): Año del mundial a consultar
--   p_grupo (OPCIONAL): Filtrar por nombre de grupo (ej: 'A', 'B', etc.)
--   p_pais (OPCIONAL): Filtrar por nombre de país
--   p_fecha (OPCIONAL): Filtrar por fecha específica de partido
-- ============================================================================

CREATE OR REPLACE PROCEDURE SP_INFO_MUNDIAL (
    p_anio_mundial  IN NUMBER,
    p_grupo         IN VARCHAR2 DEFAULT NULL,
    p_pais          IN VARCHAR2 DEFAULT NULL,
    p_fecha         IN DATE DEFAULT NULL
)
AS
    v_mundial_id        NUMBER;
    v_organizador       VARCHAR2(50);
    v_total_selecciones NUMBER;
    v_total_partidos    NUMBER;
    v_total_goles       NUMBER;
    v_existe            NUMBER;
    v_goles_eq1         NUMBER;
    v_goles_eq2         NUMBER;

    -- Variables para posiciones finales (calculadas a partir de la final)
    v_campeon           VARCHAR2(70);
    v_subcampeon        VARCHAR2(70);
    v_tercer_lugar      VARCHAR2(70);
    v_cuarto_lugar      VARCHAR2(70);

    -- Cursor para Top 5 goleadores del mundial
    CURSOR c_goleadores IS
        SELECT * FROM (
            SELECT
                j.nombre_ju AS jugador,
                p.name_pa AS pais,
                COUNT(eg.id_ev_go) AS goles
            FROM Evento_Gol eg
            INNER JOIN Evento_Partido ep ON eg.Evento_Partido_id_ev_pa = ep.id_ev_pa
            INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                        AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
            INNER JOIN Jugador j ON eg.Jugador_id_ju = j.id_ju
            INNER JOIN Posicion_Jugador pj ON j.id_ju = pj.Jugador_id_ju
            INNER JOIN Plantilla pl ON pj.Plantilla_id_pla = pl.id_pla
            INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
            -- Asegurar que sea la plantilla del mundial correcto
            INNER JOIN Partido_Plantilla pp ON pl.id_pla = pp.Plantilla_id_pla
                                            AND pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
            WHERE lm.Mundial_id_mu = v_mundial_id
            GROUP BY j.nombre_ju, p.name_pa
            ORDER BY COUNT(eg.id_ev_go) DESC
        )
        WHERE ROWNUM <= 5;

    -- Cursor para países clasificados (usando TRIM para CHAR fields)
    CURSOR c_paises_clasificados IS
        SELECT
            p.name_pa AS pais,
            TRIM(g.nombre_gr) AS grupo,
            pl.director_tecnico_pla AS director_tecnico
        FROM Pais_Clasificado_Mundial pcm
        INNER JOIN Pais p ON pcm.Pais_id_pa = p.id_pa
        INNER JOIN Grupo g ON pcm.Grupo_id_gr = g.id_gr
        LEFT JOIN (
            SELECT DISTINCT pl.Pais_id_pa, pl.director_tecnico_pla
            FROM Plantilla pl
            INNER JOIN Partido_Plantilla pp ON pl.id_pla = pp.Plantilla_id_pla
            INNER JOIN Evento_Partido ep ON pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
            INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                        AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
            WHERE lm.Mundial_id_mu = v_mundial_id
        ) pl ON pl.Pais_id_pa = p.id_pa
        WHERE pcm.Mundial_id_mu = v_mundial_id
          AND (p_grupo IS NULL OR TRIM(g.nombre_gr) = TRIM(p_grupo))
          AND (p_pais IS NULL OR UPPER(p.name_pa) LIKE '%' || UPPER(p_pais) || '%')
        ORDER BY TRIM(g.nombre_gr), p.name_pa;

    -- Cursor para premios del mundial
    CURSOR c_premios IS
        SELECT
            tp.nombre_ti_pre AS tipo_premio,
            pr.pais_pre AS pais_ganador,
            pr.entrenador_pre AS entrenador,
            (SELECT LISTAGG(j.nombre_ju, ', ') WITHIN GROUP (ORDER BY j.nombre_ju)
             FROM Premios_Jugador pj2
             INNER JOIN Jugador j ON pj2.Jugador_id_ju = j.id_ju
             WHERE pj2.Premio_id_pre = pr.id_pre) AS jugadores
        FROM Premio pr
        INNER JOIN Tipo_Premio tp ON pr.Tipo_Premio_id_ti_pre = tp.id_ti_pre
        WHERE pr.Mundial_id_mu = v_mundial_id
        ORDER BY tp.id_ti_pre;

    -- Cursor para partidos (un registro por partido)
    CURSOR c_partidos IS
        SELECT
            ep.id_ev_pa AS id_partido,
            ep.fecha_ev_pa AS fecha_partido,
            f.nombre_fa AS fase,
            (SELECT p.name_pa FROM Partido_Plantilla pp
             INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
             INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
             WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
             ORDER BY pl.id_pla FETCH FIRST 1 ROW ONLY) AS equipo1,
            (SELECT p.name_pa FROM Partido_Plantilla pp
             INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
             INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
             WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
             ORDER BY pl.id_pla DESC FETCH FIRST 1 ROW ONLY) AS equipo2,
            (SELECT pl.id_pla FROM Partido_Plantilla pp
             INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
             WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
             ORDER BY pl.id_pla FETCH FIRST 1 ROW ONLY) AS plantilla1_id,
            (SELECT pl.id_pla FROM Partido_Plantilla pp
             INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
             WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
             ORDER BY pl.id_pla DESC FETCH FIRST 1 ROW ONLY) AS plantilla2_id
        FROM Evento_Partido ep
        INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                    AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
        INNER JOIN Fase f ON lm.Fase_id_fa = f.id_fa
        WHERE lm.Mundial_id_mu = v_mundial_id
          AND (p_fecha IS NULL OR TRUNC(ep.fecha_ev_pa) = TRUNC(p_fecha))
          AND (p_pais IS NULL OR EXISTS (
              SELECT 1 FROM Partido_Plantilla pp
              INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
              INNER JOIN Pais pa ON pl.Pais_id_pa = pa.id_pa
              WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
                AND UPPER(pa.name_pa) LIKE '%' || UPPER(p_pais) || '%'
          ))
        ORDER BY ep.fecha_ev_pa, f.nombre_fa;

BEGIN
    -- Validar que el mundial exista
    SELECT COUNT(*) INTO v_existe
    FROM Mundial
    WHERE anio_mu = p_anio_mundial;

    IF v_existe = 0 THEN
        DBMS_OUTPUT.PUT_LINE('============================================================');
        DBMS_OUTPUT.PUT_LINE('ERROR: No se encontro un mundial para el anio ' || p_anio_mundial);
        DBMS_OUTPUT.PUT_LINE('============================================================');
        RETURN;
    END IF;

    -- Obtener información básica del mundial
    SELECT id_mu, organizador_mu
    INTO v_mundial_id, v_organizador
    FROM Mundial
    WHERE anio_mu = p_anio_mundial;

    -- Contar estadísticas generales
    SELECT COUNT(*) INTO v_total_selecciones
    FROM Pais_Clasificado_Mundial
    WHERE Mundial_id_mu = v_mundial_id;

    SELECT COUNT(*) INTO v_total_partidos
    FROM Evento_Partido ep
    INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
    WHERE lm.Mundial_id_mu = v_mundial_id;

    SELECT COUNT(*) INTO v_total_goles
    FROM Evento_Gol eg
    INNER JOIN Evento_Partido ep ON eg.Evento_Partido_id_ev_pa = ep.id_ev_pa
    INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
    WHERE lm.Mundial_id_mu = v_mundial_id;

    -- ========================================================================
    -- ENCABEZADO DEL REPORTE
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('          INFORMACION DEL MUNDIAL ' || p_anio_mundial);
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE(' Organizador: ' || v_organizador);
    DBMS_OUTPUT.PUT_LINE(' Total de Selecciones: ' || v_total_selecciones);
    DBMS_OUTPUT.PUT_LINE(' Total de Partidos: ' || v_total_partidos);
    DBMS_OUTPUT.PUT_LINE(' Total de Goles: ' || v_total_goles);
    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- Mostrar filtros aplicados
    IF p_grupo IS NOT NULL OR p_pais IS NOT NULL OR p_fecha IS NOT NULL THEN
        DBMS_OUTPUT.PUT_LINE('');
        DBMS_OUTPUT.PUT_LINE('FILTROS APLICADOS:');
        IF p_grupo IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('  - Grupo: ' || p_grupo);
        END IF;
        IF p_pais IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('  - Pais: ' || p_pais);
        END IF;
        IF p_fecha IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('  - Fecha: ' || TO_CHAR(p_fecha, 'DD/MM/YYYY'));
        END IF;
        DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------');
    END IF;

    -- ========================================================================
    -- SECCIÓN: POSICIONES FINALES (Campeón, Subcampeón, 3ro y 4to)
    -- Calculadas a partir de los partidos de Final y Semifinales
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('                   POSICIONES FINALES');
    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- Obtener campeón y subcampeón de la final
    BEGIN
        SELECT
            CASE WHEN goles_eq1 > goles_eq2 THEN equipo1
                 WHEN goles_eq2 > goles_eq1 THEN equipo2
                 ELSE equipo1 END,  -- En caso de empate (penales), tomar el primero
            CASE WHEN goles_eq1 > goles_eq2 THEN equipo2
                 WHEN goles_eq2 > goles_eq1 THEN equipo1
                 ELSE equipo2 END
        INTO v_campeon, v_subcampeon
        FROM (
            SELECT
                ep.id_ev_pa,
                (SELECT MIN(pp.Plantilla_id_pla) FROM Partido_Plantilla pp
                 WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa) AS plantilla1_id,
                (SELECT MAX(pp.Plantilla_id_pla) FROM Partido_Plantilla pp
                 WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa) AS plantilla2_id,
                (SELECT p.name_pa FROM Partido_Plantilla pp
                 INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
                 INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
                 WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
                 ORDER BY pl.id_pla FETCH FIRST 1 ROW ONLY) AS equipo1,
                (SELECT p.name_pa FROM Partido_Plantilla pp
                 INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
                 INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
                 WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
                 ORDER BY pl.id_pla DESC FETCH FIRST 1 ROW ONLY) AS equipo2,
                (SELECT COUNT(*) FROM Evento_Gol eg
                 WHERE eg.Evento_Partido_id_ev_pa = ep.id_ev_pa
                   AND eg.Jugador_id_ju IN (
                       SELECT pj.Jugador_id_ju FROM Posicion_Jugador pj
                       INNER JOIN Partido_Plantilla pp3 ON pj.Plantilla_id_pla = pp3.Plantilla_id_pla
                       WHERE pp3.Evento_Partido_id_ev_pa = ep.id_ev_pa
                         AND pj.Plantilla_id_pla = (SELECT MIN(pp2.Plantilla_id_pla) FROM Partido_Plantilla pp2
                                                    WHERE pp2.Evento_Partido_id_ev_pa = ep.id_ev_pa)
                   )) AS goles_eq1,
                (SELECT COUNT(*) FROM Evento_Gol eg
                 WHERE eg.Evento_Partido_id_ev_pa = ep.id_ev_pa
                   AND eg.Jugador_id_ju IN (
                       SELECT pj.Jugador_id_ju FROM Posicion_Jugador pj
                       INNER JOIN Partido_Plantilla pp3 ON pj.Plantilla_id_pla = pp3.Plantilla_id_pla
                       WHERE pp3.Evento_Partido_id_ev_pa = ep.id_ev_pa
                         AND pj.Plantilla_id_pla = (SELECT MAX(pp2.Plantilla_id_pla) FROM Partido_Plantilla pp2
                                                    WHERE pp2.Evento_Partido_id_ev_pa = ep.id_ev_pa)
                   )) AS goles_eq2
            FROM Evento_Partido ep
            INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                        AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
            INNER JOIN Fase f ON lm.Fase_id_fa = f.id_fa
            WHERE lm.Mundial_id_mu = v_mundial_id
              AND UPPER(TRIM(f.nombre_fa)) = 'FINAL'
            ORDER BY ep.fecha_ev_pa DESC
            FETCH FIRST 1 ROW ONLY
        );
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_campeon := 'No disponible';
            v_subcampeon := 'No disponible';
    END;

    -- Para 3er y 4to lugar: los perdedores de las semifinales
    -- Nota: Como no existe fase "Tercer puesto", mostramos los semifinalistas perdedores
    BEGIN
        SELECT
            LISTAGG(perdedor, ' / ') WITHIN GROUP (ORDER BY perdedor)
        INTO v_tercer_lugar
        FROM (
            SELECT
                CASE WHEN goles_eq1 < goles_eq2 THEN equipo1
                     WHEN goles_eq2 < goles_eq1 THEN equipo2
                     ELSE NULL END AS perdedor
            FROM (
                SELECT
                    ep.id_ev_pa,
                    (SELECT p.name_pa FROM Partido_Plantilla pp
                     INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
                     INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
                     WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
                     ORDER BY pl.id_pla FETCH FIRST 1 ROW ONLY) AS equipo1,
                    (SELECT p.name_pa FROM Partido_Plantilla pp
                     INNER JOIN Plantilla pl ON pp.Plantilla_id_pla = pl.id_pla
                     INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
                     WHERE pp.Evento_Partido_id_ev_pa = ep.id_ev_pa
                     ORDER BY pl.id_pla DESC FETCH FIRST 1 ROW ONLY) AS equipo2,
                    (SELECT COUNT(*) FROM Evento_Gol eg
                     WHERE eg.Evento_Partido_id_ev_pa = ep.id_ev_pa
                       AND eg.Jugador_id_ju IN (
                           SELECT pj.Jugador_id_ju FROM Posicion_Jugador pj
                           INNER JOIN Partido_Plantilla pp3 ON pj.Plantilla_id_pla = pp3.Plantilla_id_pla
                           WHERE pp3.Evento_Partido_id_ev_pa = ep.id_ev_pa
                             AND pj.Plantilla_id_pla = (SELECT MIN(pp2.Plantilla_id_pla) FROM Partido_Plantilla pp2
                                                        WHERE pp2.Evento_Partido_id_ev_pa = ep.id_ev_pa)
                       )) AS goles_eq1,
                    (SELECT COUNT(*) FROM Evento_Gol eg
                     WHERE eg.Evento_Partido_id_ev_pa = ep.id_ev_pa
                       AND eg.Jugador_id_ju IN (
                           SELECT pj.Jugador_id_ju FROM Posicion_Jugador pj
                           INNER JOIN Partido_Plantilla pp3 ON pj.Plantilla_id_pla = pp3.Plantilla_id_pla
                           WHERE pp3.Evento_Partido_id_ev_pa = ep.id_ev_pa
                             AND pj.Plantilla_id_pla = (SELECT MAX(pp2.Plantilla_id_pla) FROM Partido_Plantilla pp2
                                                        WHERE pp2.Evento_Partido_id_ev_pa = ep.id_ev_pa)
                       )) AS goles_eq2
                FROM Evento_Partido ep
                INNER JOIN Llave_Mundial lm ON ep.Llave_Mundial_id_mu = lm.Mundial_id_mu
                                            AND ep.Llave_Mundial_id_fa = lm.Fase_id_fa
                INNER JOIN Fase f ON lm.Fase_id_fa = f.id_fa
                WHERE lm.Mundial_id_mu = v_mundial_id
                  AND UPPER(TRIM(f.nombre_fa)) = 'SEMIFINALES'
            ) partidos_semi
        ) resultados
        WHERE perdedor IS NOT NULL;
        v_cuarto_lugar := '(Semifinalistas eliminados)';
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            v_tercer_lugar := 'No disponible';
            v_cuarto_lugar := 'No disponible';
    END;

    DBMS_OUTPUT.PUT_LINE('  1. CAMPEON:       ' || NVL(v_campeon, 'No disponible'));
    DBMS_OUTPUT.PUT_LINE('  2. SUBCAMPEON:    ' || NVL(v_subcampeon, 'No disponible'));
    DBMS_OUTPUT.PUT_LINE('  3-4. SEMIFINALES: ' || NVL(v_tercer_lugar, 'No disponible'));

    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- ========================================================================
    -- SECCIÓN: TOP 5 GOLEADORES
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('                   TOP 5 GOLEADORES');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE(RPAD('POS', 5) || RPAD('JUGADOR', 35) || RPAD('PAIS', 20) || 'GOLES');
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------');

    DECLARE
        v_ranking NUMBER := 0;
    BEGIN
        FOR r_gol IN c_goleadores LOOP
            v_ranking := v_ranking + 1;
            DBMS_OUTPUT.PUT_LINE(
                RPAD(TO_CHAR(v_ranking), 5) ||
                RPAD(NVL(SUBSTR(r_gol.jugador, 1, 33), '-'), 35) ||
                RPAD(NVL(SUBSTR(r_gol.pais, 1, 18), '-'), 20) ||
                TO_CHAR(r_gol.goles)
            );
        END LOOP;
    END;

    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- ========================================================================
    -- SECCIÓN: PREMIOS
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('                       PREMIOS');
    DBMS_OUTPUT.PUT_LINE('================================================================');

    FOR r_premio IN c_premios LOOP
        DBMS_OUTPUT.PUT_LINE('');
        DBMS_OUTPUT.PUT_LINE('  ' || r_premio.tipo_premio);
        IF r_premio.pais_ganador IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('    Pais: ' || r_premio.pais_ganador);
        END IF;
        IF r_premio.entrenador IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('    Entrenador: ' || r_premio.entrenador);
        END IF;
        IF r_premio.jugadores IS NOT NULL THEN
            DBMS_OUTPUT.PUT_LINE('    Jugador(es): ' || SUBSTR(r_premio.jugadores, 1, 50));
        END IF;
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- ========================================================================
    -- SECCIÓN: SELECCIONES CLASIFICADAS
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('                  SELECCIONES CLASIFICADAS');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE(RPAD('GRUPO', 8) || RPAD('SELECCION', 30) || 'DIRECTOR TECNICO');
    DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------');

    FOR r_pais IN c_paises_clasificados LOOP
        DBMS_OUTPUT.PUT_LINE(
            RPAD(NVL(r_pais.grupo, '-'), 8) ||
            RPAD(NVL(r_pais.pais, '-'), 30) ||
            NVL(SUBSTR(r_pais.director_tecnico, 1, 25), '-')
        );
    END LOOP;

    DBMS_OUTPUT.PUT_LINE('================================================================');

    -- ========================================================================
    -- SECCIÓN: PARTIDOS Y RESULTADOS
    -- ========================================================================
    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('                   PARTIDOS Y RESULTADOS');
    DBMS_OUTPUT.PUT_LINE('================================================================');

    FOR r_partido IN c_partidos LOOP
        -- Calcular goles de cada equipo (asegurando que solo contamos jugadores de la plantilla del partido)
        SELECT COUNT(*) INTO v_goles_eq1
        FROM Evento_Gol eg
        WHERE eg.Evento_Partido_id_ev_pa = r_partido.id_partido
          AND eg.Jugador_id_ju IN (
              SELECT pj.Jugador_id_ju FROM Posicion_Jugador pj
              WHERE pj.Plantilla_id_pla = r_partido.plantilla1_id
          );

        SELECT COUNT(*) INTO v_goles_eq2
        FROM Evento_Gol eg
        WHERE eg.Evento_Partido_id_ev_pa = r_partido.id_partido
          AND eg.Jugador_id_ju IN (
              SELECT pj.Jugador_id_ju FROM Posicion_Jugador pj
              WHERE pj.Plantilla_id_pla = r_partido.plantilla2_id
          );

        DBMS_OUTPUT.PUT_LINE('');
        DBMS_OUTPUT.PUT_LINE('----------------------------------------------------------------');
        DBMS_OUTPUT.PUT_LINE('Fecha: ' || TO_CHAR(r_partido.fecha_partido, 'DD/MM/YYYY') ||
                             '  |  Fase: ' || NVL(r_partido.fase, '-'));
        DBMS_OUTPUT.PUT_LINE('');
        DBMS_OUTPUT.PUT_LINE('  ' || RPAD(NVL(r_partido.equipo1, '-'), 25) ||
                             '  ' || LPAD(TO_CHAR(v_goles_eq1), 2) ||
                             ' - ' || RPAD(TO_CHAR(v_goles_eq2), 2) ||
                             '  ' || NVL(r_partido.equipo2, '-'));

        -- Mostrar goles del partido
        DBMS_OUTPUT.PUT_LINE('');
        DBMS_OUTPUT.PUT_LINE('  GOLES:');
        FOR r_gol IN (
            SELECT
                j.nombre_ju AS goleador,
                p.name_pa AS pais,
                eg.tiempo_gol AS minuto,
                eg.penal AS es_penal
            FROM Evento_Gol eg
            INNER JOIN Jugador j ON eg.Jugador_id_ju = j.id_ju
            INNER JOIN Posicion_Jugador pj ON j.id_ju = pj.Jugador_id_ju
                AND pj.Plantilla_id_pla IN (r_partido.plantilla1_id, r_partido.plantilla2_id)
            INNER JOIN Plantilla pl ON pj.Plantilla_id_pla = pl.id_pla
            INNER JOIN Pais p ON pl.Pais_id_pa = p.id_pa
            WHERE eg.Evento_Partido_id_ev_pa = r_partido.id_partido
            ORDER BY eg.tiempo_gol
        ) LOOP
            DBMS_OUTPUT.PUT_LINE('    Min ' || RPAD(NVL(r_gol.minuto, '-'), 5) ||
                                 ' - ' || RPAD(NVL(SUBSTR(r_gol.goleador, 1, 28), '-'), 30) ||
                                 ' (' || NVL(SUBSTR(r_gol.pais, 1, 12), '-') || ')' ||
                                 CASE WHEN r_gol.es_penal = 1 THEN ' [Penal]' ELSE '' END);
        END LOOP;

        -- Mostrar tarjetas del partido
        DBMS_OUTPUT.PUT_LINE('  TARJETAS:');
        FOR r_tarjeta IN (
            SELECT DISTINCT
                j.nombre_ju AS jugador,
                tt.color_tarjeta AS tipo_tarjeta,
                ef.minuto_falta AS minuto
            FROM Evento_Falta ef
            INNER JOIN Tipo_Tarjeta tt ON ef.Tipo_Tarjeta_id_ti_ta = tt.id_ti_ta
            INNER JOIN Partido_Plantilla pp ON ef.Evento_Partido_id_ev_pa = pp.Evento_Partido_id_ev_pa
            INNER JOIN Posicion_Jugador pj ON pp.Plantilla_id_pla = pj.Plantilla_id_pla
            INNER JOIN Jugador j ON pj.Jugador_id_ju = j.id_ju
            WHERE ef.Evento_Partido_id_ev_pa = r_partido.id_partido
              AND pp.Plantilla_id_pla IN (r_partido.plantilla1_id, r_partido.plantilla2_id)
            ORDER BY ef.minuto_falta
            FETCH FIRST 10 ROWS ONLY
        ) LOOP
            DBMS_OUTPUT.PUT_LINE('    Min ' || RPAD(NVL(r_tarjeta.minuto, '-'), 5) ||
                                 ' - ' || RPAD(NVL(SUBSTR(r_tarjeta.jugador, 1, 23), '-'), 25) ||
                                 ' [' || NVL(r_tarjeta.tipo_tarjeta, '-') || ']');
        END LOOP;

    END LOOP;

    DBMS_OUTPUT.PUT_LINE('');
    DBMS_OUTPUT.PUT_LINE('================================================================');
    DBMS_OUTPUT.PUT_LINE('                    FIN DEL REPORTE');
    DBMS_OUTPUT.PUT_LINE('================================================================');

EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('ERROR: No se encontraron datos para el mundial ' || p_anio_mundial);
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('ERROR: ' || SQLERRM);
END SP_INFO_MUNDIAL;
/

-- ============================================================================
-- EJEMPLOS DE USO:
-- ============================================================================
-- 1. Ver toda la información del mundial 2022:
--    EXEC SP_INFO_MUNDIAL(2022);
--
-- 2. Filtrar por grupo específico:
--    EXEC SP_INFO_MUNDIAL(2022, 'A');
--
-- 3. Filtrar por país:
--    EXEC SP_INFO_MUNDIAL(2022, NULL, 'Argentina');
--
-- 4. Filtrar por fecha específica:
--    EXEC SP_INFO_MUNDIAL(2022, NULL, NULL, TO_DATE('18/12/2022', 'DD/MM/YYYY'));
--
-- 5. Combinación de filtros (grupo y país):
--    EXEC SP_INFO_MUNDIAL(2022, 'C', 'Argentina');
-- ============================================================================

-- Habilitar salida de DBMS_OUTPUT
SET SERVEROUTPUT ON SIZE UNLIMITED;
