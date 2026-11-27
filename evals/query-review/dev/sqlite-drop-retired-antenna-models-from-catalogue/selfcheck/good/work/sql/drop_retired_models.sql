-- Remove retired models nothing refers to (docs/catalogue.md): no installed antenna, no spare stock.
-- Foreign keys are not enforced on these connections, so the checks have to be explicit.
DELETE FROM models
WHERE status = 'retired'
  AND NOT EXISTS (SELECT 1 FROM antennas a WHERE a.model_id = models.id)
  AND NOT EXISTS (SELECT 1 FROM spares s WHERE s.model_code = models.code);
