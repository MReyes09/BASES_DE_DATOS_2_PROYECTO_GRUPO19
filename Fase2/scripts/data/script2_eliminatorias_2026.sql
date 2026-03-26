-- =====================================================
-- SCRIPT 2: Partidos Simulados - Fases Eliminatorias
-- Mundial 2026 (id_mu=1)
-- 8 Octavos (Fase 2) + 4 Cuartos (Fase 3) + 2 Semis (Fase 4) + 1 Final (Fase 5)
-- =====================================================
-- IDs base (continuan desde Script 1):
--   Evento_Partido:         980 - 994
--   Evento_Gol:             2761 - 2810
--   Evento_Falta:           2684 - 2733
--   Evento_Cambio_Jugador:  3859 - 3903
--   Cambio_Jugador:         7717 - 7806
-- =====================================================

-- =========================
-- EVENTO_PARTIDO (15 partidos)
-- =========================

-- Octavos de Final (Fase 2)
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (980, TO_DATE('25/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (981, TO_DATE('25/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (982, TO_DATE('26/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (983, TO_DATE('26/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (984, TO_DATE('27/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (985, TO_DATE('27/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (986, TO_DATE('28/06/2026', 'DD/MM/YYYY'), 1, 2);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (987, TO_DATE('28/06/2026', 'DD/MM/YYYY'), 1, 2);

-- Cuartos de Final (Fase 3)
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (988, TO_DATE('02/07/2026', 'DD/MM/YYYY'), 1, 3);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (989, TO_DATE('02/07/2026', 'DD/MM/YYYY'), 1, 3);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (990, TO_DATE('03/07/2026', 'DD/MM/YYYY'), 1, 3);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (991, TO_DATE('03/07/2026', 'DD/MM/YYYY'), 1, 3);

-- Semifinales (Fase 4)
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (992, TO_DATE('06/07/2026', 'DD/MM/YYYY'), 1, 4);
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (993, TO_DATE('07/07/2026', 'DD/MM/YYYY'), 1, 4);

-- Final (Fase 5)
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (994, TO_DATE('10/07/2026', 'DD/MM/YYYY'), 1, 5);

-- =========================
-- PARTIDO_PLANTILLA (2 equipos por partido = 30 inserts)
-- =========================

-- Octavos
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (35, 980);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (206, 980);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (3, 981);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (389, 981);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (72, 982);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (283, 982);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (187, 983);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (315, 983);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (89, 984);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (312, 984);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (400, 985);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (356, 985);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (47, 986);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (304, 986);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (130, 987);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (385, 987);

-- Cuartos
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (35, 988);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (72, 988);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (315, 989);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (89, 989);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (400, 990);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (47, 990);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (130, 991);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (3, 991);

-- Semifinales
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (35, 992);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (89, 992);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (47, 993);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (130, 993);

-- Final
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (35, 994);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (130, 994);

-- =========================
-- EVENTO_GOL (50 goles en 15 partidos)
-- =========================

-- Octavo 980: Resultado 2-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2761, 980, 7317, '18', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2762, 980, 2454, '73', '1', 0);

-- Octavo 981: Resultado 1-1 (clasifica 3 por penales)
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2763, 981, 2179, '32', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2764, 981, 4989, '58', '1', 0);

-- Octavo 982: Resultado 3-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2765, 982, 2631, '10', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2766, 982, 5989, '35', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2767, 982, 4404, '52', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2768, 982, 2631, '79', '1', 0);

-- Octavo 983: Resultado 0-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2769, 983, 1539, '88', '1', 0);

-- Octavo 984: Resultado 2-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2770, 984, 3468, '15', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2771, 984, 6124, '44', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2772, 984, 3468, '67', '1', 1);

-- Octavo 985: Resultado 1-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2773, 985, 5996, '41', '0', 0);

-- Octavo 986: Resultado 4-2
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2774, 986, 4443, '7', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2775, 986, 6002, '22', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2776, 986, 4446, '51', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2777, 986, 5440, '63', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2778, 986, 2856, '75', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2779, 986, 4443, '85', '1', 1);

-- Octavo 987: Resultado 2-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2780, 987, 2828, '30', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2781, 987, 1480, '61', '1', 0);

-- Cuarto 988: Resultado 2-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2782, 988, 7317, '14', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2783, 988, 2631, '37', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2784, 988, 5272, '82', '1', 1);

-- Cuarto 989: Resultado 0-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2785, 989, 3468, '56', '1', 0);

-- Cuarto 990: Resultado 1-2
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2786, 990, 5996, '20', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2787, 990, 4443, '48', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2788, 990, 4446, '90+3', '1', 0);

-- Cuarto 991: Resultado 3-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2789, 991, 2828, '11', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2790, 991, 2179, '33', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2791, 991, 1480, '59', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2792, 991, 2828, '78', '1', 0);

-- Semifinal 992: Resultado 2-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2793, 992, 7317, '27', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2794, 992, 5272, '64', '1', 0);

-- Semifinal 993: Resultado 1-3
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2795, 993, 4443, '19', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2796, 993, 2828, '25', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2797, 993, 1480, '53', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2798, 993, 2828, '71', '1', 0);

-- Final 994: Resultado 3-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2799, 994, 7317, '22', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2800, 994, 2828, '38', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2801, 994, 5272, '57', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2802, 994, 1480, '75', '1', 1);

-- =========================
-- EVENTO_FALTA (50 faltas/tarjetas)
-- Tipo_Tarjeta: 1=AMARILLA, 2=ROJA
-- =========================

-- Octavo 980
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2684, 980, 1, '12', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2685, 980, 1, '44', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2686, 980, 1, '68', 1);

-- Octavo 981
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2687, 981, 1, '21', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2688, 981, 1, '55', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2689, 981, 2, '78', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2690, 981, 1, '85', 1);

-- Octavo 982
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2691, 982, 1, '17', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2692, 982, 1, '39', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2693, 982, 1, '72', 1);

-- Octavo 983
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2694, 983, 1, '30', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2695, 983, 1, '62', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2696, 983, 1, '80', 1);

-- Octavo 984
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2697, 984, 1, '8', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2698, 984, 1, '36', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2699, 984, 2, '59', 1);

-- Octavo 985
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2700, 985, 1, '25', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2701, 985, 1, '53', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2702, 985, 1, '77', 1);

-- Octavo 986
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2703, 986, 1, '15', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2704, 986, 1, '34', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2705, 986, 1, '56', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2706, 986, 2, '82', 1);

-- Octavo 987
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2707, 987, 1, '19', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2708, 987, 1, '48', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2709, 987, 1, '70', 1);

-- Cuarto 988
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2710, 988, 1, '10', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2711, 988, 1, '33', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2712, 988, 1, '58', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2713, 988, 2, '80', 1);

-- Cuarto 989
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2714, 989, 1, '23', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2715, 989, 1, '45', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2716, 989, 1, '67', 1);

-- Cuarto 990
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2717, 990, 1, '14', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2718, 990, 1, '41', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2719, 990, 1, '73', 1);

-- Cuarto 991
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2720, 991, 1, '18', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2721, 991, 1, '52', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2722, 991, 1, '85', 1);

-- Semifinal 992
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2723, 992, 1, '16', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2724, 992, 1, '38', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2725, 992, 1, '61', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2726, 992, 2, '88', 1);

-- Semifinal 993
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2727, 993, 1, '11', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2728, 993, 1, '42', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2729, 993, 1, '65', 1);

-- Final 994
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2730, 994, 1, '9', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2731, 994, 1, '31', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2732, 994, 1, '55', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2733, 994, 2, '83', 1);

-- =========================
-- EVENTO_CAMBIO_JUGADOR (45 eventos de cambio)
-- =========================

-- Octavo 980 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3859, 980);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3860, 980);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3861, 980);

-- Octavo 981 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3862, 981);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3863, 981);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3864, 981);

-- Octavo 982 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3865, 982);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3866, 982);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3867, 982);

-- Octavo 983 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3868, 983);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3869, 983);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3870, 983);

-- Octavo 984 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3871, 984);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3872, 984);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3873, 984);

-- Octavo 985 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3874, 985);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3875, 985);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3876, 985);

-- Octavo 986 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3877, 986);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3878, 986);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3879, 986);

-- Octavo 987 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3880, 987);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3881, 987);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3882, 987);

-- Cuarto 988 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3883, 988);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3884, 988);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3885, 988);

-- Cuarto 989 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3886, 989);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3887, 989);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3888, 989);

-- Cuarto 990 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3889, 990);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3890, 990);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3891, 990);

-- Cuarto 991 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3892, 991);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3893, 991);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3894, 991);

-- Semifinal 992 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3895, 992);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3896, 992);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3897, 992);

-- Semifinal 993 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3898, 993);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3899, 993);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3900, 993);

-- Final 994 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3901, 994);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3902, 994);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3903, 994);

-- =========================
-- CAMBIO_JUGADOR (2 jugadores por evento: sale 1, entra 1)
-- Total: 90 inserts
-- =========================

-- Octavo 980
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7717, 3859, 6149, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7718, 3859, 1185, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7719, 3860, 8445, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7720, 3860, 6689, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7721, 3861, 7902, '78');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7722, 3861, 2828, '78');

-- Octavo 981
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7723, 3862, 1480, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7724, 3862, 3554, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7725, 3863, 1462, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7726, 3863, 5222, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7727, 3864, 6289, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7728, 3864, 7997, '80');

-- Octavo 982
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7729, 3865, 4895, '50');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7730, 3865, 1415, '50');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7731, 3866, 2370, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7732, 3866, 2693, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7733, 3867, 2227, '77');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7734, 3867, 4004, '77');

-- Octavo 983
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7735, 3868, 3019, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7736, 3868, 4568, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7737, 3869, 8145, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7738, 3869, 792, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7739, 3870, 5200, '82');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7740, 3870, 2022, '82');

-- Octavo 984
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7741, 3871, 7072, '54');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7742, 3871, 2741, '54');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7743, 3872, 6981, '66');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7744, 3872, 3383, '66');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7745, 3873, 4517, '79');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7746, 3873, 821, '79');

-- Octavo 985
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7747, 3874, 6238, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7748, 3874, 7027, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7749, 3875, 5065, '69');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7750, 3875, 4798, '69');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7751, 3876, 7054, '81');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7752, 3876, 6630, '81');

-- Octavo 986
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7753, 3877, 3442, '52');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7754, 3877, 7985, '52');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7755, 3878, 7986, '67');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7756, 3878, 6579, '67');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7757, 3879, 7682, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7758, 3879, 547, '80');

-- Octavo 987
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7759, 3880, 3484, '53');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7760, 3880, 7317, '53');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7761, 3881, 7420, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7762, 3881, 2454, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7763, 3882, 5272, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7764, 3882, 6995, '80');

-- Cuarto 988
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7765, 3883, 6149, '57');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7766, 3883, 1185, '57');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7767, 3884, 8445, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7768, 3884, 6689, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7769, 3885, 2631, '83');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7770, 3885, 4989, '83');

-- Cuarto 989
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7771, 3886, 1539, '54');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7772, 3886, 6124, '54');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7773, 3887, 3185, '66');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7774, 3887, 2340, '66');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7775, 3888, 2862, '78');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7776, 3888, 2495, '78');

-- Cuarto 990
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7777, 3889, 5996, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7778, 3889, 6411, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7779, 3890, 4483, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7780, 3890, 1809, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7781, 3891, 1519, '82');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7782, 3891, 6002, '82');

-- Cuarto 991
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7783, 3892, 4004, '52');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7784, 3892, 3019, '52');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7785, 3893, 4568, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7786, 3893, 8145, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7787, 3894, 792, '79');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7788, 3894, 5200, '79');

-- Semifinal 992
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7789, 3895, 7902, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7790, 3895, 2828, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7791, 3896, 6689, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7792, 3896, 8445, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7793, 3897, 3468, '83');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7794, 3897, 6124, '83');

-- Semifinal 993
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7795, 3898, 5440, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7796, 3898, 1588, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7797, 3899, 3554, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7798, 3899, 1462, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7799, 3900, 5222, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7800, 3900, 6289, '80');

-- Final 994
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7801, 3901, 6149, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7802, 3901, 1185, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7803, 3902, 2179, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7804, 3902, 4989, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7805, 3903, 2631, '84');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7806, 3903, 5989, '84');

COMMIT;
