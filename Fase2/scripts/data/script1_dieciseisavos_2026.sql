-- =====================================================
-- SCRIPT 1: Partidos Simulados - Dieciseisavos de Final
-- Mundial 2026 (id_mu=1, Fase_id_fa=1)
-- 15 partidos con goles, faltas, cambios
-- =====================================================
-- IDs base:
--   Evento_Partido:         965 - 979
--   Evento_Gol:             2721 - 2760
--   Evento_Falta:           2639 - 2683
--   Evento_Cambio_Jugador:  3818 - 3858
--   Cambio_Jugador:         7635 - 7716
-- =====================================================

-- =========================
-- EVENTO_PARTIDO (15 partidos)
-- =========================

-- Partido 1: 14/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (965, TO_DATE('14/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 2: 14/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (966, TO_DATE('14/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 3: 15/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (967, TO_DATE('15/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 4: 15/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (968, TO_DATE('15/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 5: 16/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (969, TO_DATE('16/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 6: 16/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (970, TO_DATE('16/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 7: 17/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (971, TO_DATE('17/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 8: 17/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (972, TO_DATE('17/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 9: 18/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (973, TO_DATE('18/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 10: 18/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (974, TO_DATE('18/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 11: 19/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (975, TO_DATE('19/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 12: 19/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (976, TO_DATE('19/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 13: 20/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (977, TO_DATE('20/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 14: 20/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (978, TO_DATE('20/06/2026', 'DD/MM/YYYY'), 1, 1);
-- Partido 15: 21/06/2026
INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES (979, TO_DATE('21/06/2026', 'DD/MM/YYYY'), 1, 1);

-- =========================
-- PARTIDO_PLANTILLA (2 equipos por partido = 30 inserts)
-- =========================

-- Partido 965: Plantilla 35 (Argentina-Scaloni) vs Plantilla 110 
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (35, 965);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (110, 965);
-- Partido 966: Plantilla 3 (Alemania-Loew) vs Plantilla 206
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (3, 966);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (206, 966);
-- Partido 967: Plantilla 72 vs Plantilla 389
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (72, 967);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (389, 967);
-- Partido 968: Plantilla 61 vs Plantilla 283
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (61, 968);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (283, 968);
-- Partido 969: Plantilla 187 vs Plantilla 337
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (187, 969);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (337, 969);
-- Partido 970: Plantilla 89 vs Plantilla 315
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (89, 970);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (315, 970);
-- Partido 971: Plantilla 400 vs Plantilla 312
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (400, 971);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (312, 971);
-- Partido 972: Plantilla 5 vs Plantilla 356
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (5, 972);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (356, 972);
-- Partido 973: Plantilla 47 vs Plantilla 201
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (47, 973);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (201, 973);
-- Partido 974: Plantilla 223 vs Plantilla 304
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (223, 974);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (304, 974);
-- Partido 975: Plantilla 130 vs Plantilla 199
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (130, 975);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (199, 975);
-- Partido 976: Plantilla 39 vs Plantilla 385
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (39, 976);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (385, 976);
-- Partido 977: Plantilla 390 vs Plantilla 34
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (390, 977);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (34, 977);
-- Partido 978: Plantilla 110 vs Plantilla 72
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (110, 978);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (72, 978);
-- Partido 979: Plantilla 206 vs Plantilla 61
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (206, 979);
INSERT INTO Partido_Plantilla (Plantilla_id_pla, Evento_Partido_id_ev_pa) VALUES (61, 979);

-- =========================
-- EVENTO_GOL (40 goles en 15 partidos)
-- =========================

-- Partido 965: Resultado 2-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2721, 965, 7317, '23', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2722, 965, 2454, '45', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2723, 965, 5272, '67', '1', 0);

-- Partido 966: Resultado 1-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2724, 966, 2179, '55', '1', 0);

-- Partido 967: Resultado 3-2
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2725, 967, 4989, '12', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2726, 967, 2631, '30', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2727, 967, 5989, '44', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2728, 967, 4404, '52', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2729, 967, 4368, '78', '1', 1);

-- Partido 968: Resultado 0-0 (sin goles)

-- Partido 969: Resultado 1-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2730, 969, 5200, '38', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2731, 969, 2022, '72', '1', 0);

-- Partido 970: Resultado 2-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2732, 970, 1539, '29', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2733, 970, 3468, '61', '1', 0);

-- Partido 971: Resultado 4-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2734, 971, 5996, '8', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2735, 971, 6411, '22', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2736, 971, 4483, '51', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2737, 971, 1809, '63', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2738, 971, 1519, '88', '1', 0);

-- Partido 972: Resultado 1-2
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2739, 972, 6002, '19', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2740, 972, 2856, '45', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2741, 972, 4315, '68', '1', 0);

-- Partido 973: Resultado 2-2
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2742, 973, 4443, '11', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2743, 973, 4446, '35', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2744, 973, 5440, '59', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2745, 973, 1588, '82', '1', 1);

-- Partido 974: Resultado 0-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2746, 974, 6149, '90+2', '1', 0);

-- Partido 975: Resultado 3-0
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2747, 975, 2828, '15', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2748, 975, 2179, '42', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2749, 975, 1480, '71', '1', 0);

-- Partido 976: Resultado 1-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2750, 976, 2631, '33', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2751, 976, 5989, '67', '1', 0);

-- Partido 977: Resultado 2-1
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2752, 977, 2370, '25', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2753, 977, 2693, '53', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2754, 977, 2227, '77', '1', 0);

-- Partido 978: Resultado 0-2
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2755, 978, 2022, '40', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2756, 978, 7072, '62', '1', 0);

-- Partido 979: Resultado 1-3
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2757, 979, 821, '5', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2758, 979, 1539, '28', '0', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2759, 979, 3468, '55', '1', 0);
INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES (2760, 979, 6124, '81', '1', 0);

-- =========================
-- EVENTO_FALTA (45 faltas/tarjetas en 15 partidos)
-- Tipo_Tarjeta: 1=AMARILLA, 2=ROJA
-- =========================

-- Partido 965
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2639, 965, 1, '34', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2640, 965, 1, '56', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2641, 965, 2, '78', 1);

-- Partido 966
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2642, 966, 1, '22', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2643, 966, 1, '61', 1);

-- Partido 967
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2644, 967, 1, '18', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2645, 967, 1, '40', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2646, 967, 1, '65', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2647, 967, 2, '88', 1);

-- Partido 968
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2648, 968, 1, '15', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2649, 968, 1, '33', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2650, 968, 1, '71', 1);

-- Partido 969
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2651, 969, 1, '25', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2652, 969, 1, '50', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2653, 969, 1, '85', 1);

-- Partido 970
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2654, 970, 1, '42', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2655, 970, 1, '58', 1);

-- Partido 971
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2656, 971, 1, '35', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2657, 971, 1, '55', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2658, 971, 2, '70', 1);

-- Partido 972
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2659, 972, 1, '27', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2660, 972, 1, '52', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2661, 972, 1, '76', 1);

-- Partido 973
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2662, 973, 1, '20', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2663, 973, 1, '47', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2664, 973, 2, '75', 1);

-- Partido 974
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2665, 974, 1, '10', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2666, 974, 1, '38', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2667, 974, 1, '62', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2668, 974, 1, '80', 1);

-- Partido 975
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2669, 975, 1, '28', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2670, 975, 1, '55', 1);

-- Partido 976
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2671, 976, 1, '12', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2672, 976, 1, '45', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2673, 976, 1, '68', 1);

-- Partido 977
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2674, 977, 1, '30', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2675, 977, 1, '60', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2676, 977, 2, '85', 1);

-- Partido 978
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2677, 978, 1, '18', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2678, 978, 1, '50', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2679, 978, 1, '73', 1);

-- Partido 979
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2680, 979, 1, '14', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2681, 979, 1, '37', 0);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2682, 979, 1, '63', 1);
INSERT INTO Evento_Falta (id_ev_fa, Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo) VALUES (2683, 979, 2, '89', 1);

-- =========================
-- EVENTO_CAMBIO_JUGADOR (41 eventos de cambio)
-- =========================

-- Partido 965 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3818, 965);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3819, 965);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3820, 965);

-- Partido 966 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3821, 966);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3822, 966);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3823, 966);

-- Partido 967 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3824, 967);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3825, 967);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3826, 967);

-- Partido 968 (2 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3827, 968);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3828, 968);

-- Partido 969 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3829, 969);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3830, 969);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3831, 969);

-- Partido 970 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3832, 970);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3833, 970);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3834, 970);

-- Partido 971 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3835, 971);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3836, 971);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3837, 971);

-- Partido 972 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3838, 972);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3839, 972);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3840, 972);

-- Partido 973 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3841, 973);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3842, 973);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3843, 973);

-- Partido 974 (2 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3844, 974);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3845, 974);

-- Partido 975 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3846, 975);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3847, 975);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3848, 975);

-- Partido 976 (2 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3849, 976);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3850, 976);

-- Partido 977 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3851, 977);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3852, 977);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3853, 977);

-- Partido 978 (2 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3854, 978);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3855, 978);

-- Partido 979 (3 cambios)
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3856, 979);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3857, 979);
INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, Evento_Partido_id_ev_pa) VALUES (3858, 979);

-- =========================
-- CAMBIO_JUGADOR (2 jugadores por evento de cambio: sale 1, entra 1)
-- Total: 82 inserts
-- =========================

-- Partido 965
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7635, 3818, 6149, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7636, 3818, 1185, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7637, 3819, 8445, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7638, 3819, 6689, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7639, 3820, 7902, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7640, 3820, 2828, '80');

-- Partido 966
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7641, 3821, 1480, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7642, 3821, 3554, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7643, 3822, 1462, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7644, 3822, 5222, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7645, 3823, 6289, '82');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7646, 3823, 7997, '82');

-- Partido 967
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7647, 3824, 4895, '46');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7648, 3824, 1415, '46');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7649, 3825, 2370, '62');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7650, 3825, 2693, '62');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7651, 3826, 2227, '75');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7652, 3826, 4004, '75');

-- Partido 968
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7653, 3827, 3019, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7654, 3827, 4568, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7655, 3828, 8145, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7656, 3828, 792, '68');

-- Partido 969
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7657, 3829, 7072, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7658, 3829, 2741, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7659, 3830, 6981, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7660, 3830, 3383, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7661, 3831, 4517, '83');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7662, 3831, 821, '83');

-- Partido 970
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7663, 3832, 6124, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7664, 3832, 3185, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7665, 3833, 2340, '67');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7666, 3833, 2862, '67');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7667, 3834, 2495, '78');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7668, 3834, 692, '78');

-- Partido 971
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7669, 3835, 6238, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7670, 3835, 7027, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7671, 3836, 5065, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7672, 3836, 4798, '72');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7673, 3837, 7054, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7674, 3837, 6630, '80');

-- Partido 972
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7675, 3838, 3442, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7676, 3838, 7985, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7677, 3839, 7986, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7678, 3839, 6579, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7679, 3840, 7682, '79');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7680, 3840, 547, '79');

-- Partido 973
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7681, 3841, 3484, '54');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7682, 3841, 7317, '54');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7683, 3842, 7420, '66');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7684, 3842, 2454, '66');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7685, 3843, 5272, '78');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7686, 3843, 6995, '78');

-- Partido 974
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7687, 3844, 1185, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7688, 3844, 8445, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7689, 3845, 6689, '75');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7690, 3845, 7902, '75');

-- Partido 975
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7691, 3846, 3554, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7692, 3846, 1462, '60');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7693, 3847, 5222, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7694, 3847, 6289, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7695, 3848, 7997, '82');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7696, 3848, 4989, '82');

-- Partido 976
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7697, 3849, 4404, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7698, 3849, 4368, '58');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7699, 3850, 4895, '73');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7700, 3850, 1415, '73');

-- Partido 977
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7701, 3851, 4004, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7702, 3851, 3019, '56');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7703, 3852, 4568, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7704, 3852, 8145, '68');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7705, 3853, 792, '80');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7706, 3853, 5200, '80');

-- Partido 978
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7707, 3854, 2741, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7708, 3854, 6981, '55');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7709, 3855, 3383, '70');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7710, 3855, 4517, '70');

-- Partido 979
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7711, 3856, 3185, '52');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7712, 3856, 2340, '52');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7713, 3857, 2862, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7714, 3857, 2495, '65');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7715, 3858, 692, '78');
INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju) VALUES (7716, 3858, 5996, '78');

COMMIT;
