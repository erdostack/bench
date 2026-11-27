-- ticket: MOVE-204 objects back from STORE-B to G7 after the refit (31 objects)
-- reviewer: p.dube
UPDATE edges SET dst = (SELECT id FROM nodes WHERE code = 'G7'), since = '2026-06-02'
WHERE kind = 'located_in' AND dst = (SELECT id FROM nodes WHERE code = 'STORE-B')
  AND src IN (SELECT id FROM nodes WHERE code IN ('1931.4.17', '1931.4.18', '1958.102.3'));
