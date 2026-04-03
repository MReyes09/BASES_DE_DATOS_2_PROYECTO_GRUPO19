# Persona 1 — DBA / Carga & Backups
Es el cuello de botella del proyecto, por eso debe empezar *ya*.

- [x] Crear las *tablas LOG* (una por cada tabla del modelo, ~20 tablas) con triggers o inserts manuales que registren fragmentación
- [ ] Configurar el entorno Oracle para RMAN: rutas de almacenamiento de backups
- [ ] Ejecutar la *carga de datos simulada* en 3 días:
  - Día 1 y 2: insertar partidos y resultados
  - Día 3: UPDATE de países a UPPER(name_pa)
- [ ] Al final de cada día: *full backup + incremental/diferencial* vía consola (RMAN)
- [ ] Tomar capturas de SELECT * y SELECT COUNT(*) por tabla después de cada carga (con fecha/hora visible)