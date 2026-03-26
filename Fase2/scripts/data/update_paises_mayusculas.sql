-- =============================================================
-- UPDATE: Convertir nombres de paises a MAYUSCULAS
-- Usa UPPER() + NLS para manejar tildes y caracteres especiales
-- Oracle Database 21c
-- =============================================================

UPDATE Pais SET name_pa = UPPER(name_pa);

COMMIT;
