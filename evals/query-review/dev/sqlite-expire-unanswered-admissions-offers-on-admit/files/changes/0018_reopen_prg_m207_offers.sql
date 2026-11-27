-- reason: ADM-2950 offers for PRG-M207 were expired by mistake during the October outage
-- check: SELECT count(*) FROM edges WHERE kind = 'applied_to' AND status = 'expired' AND dst = (SELECT id FROM nodes WHERE code = 'PRG-M207') AND reply_by >= '2026-10-20'
UPDATE edges SET status = 'offer'
WHERE id IN (SELECT id FROM edges
             WHERE kind = 'applied_to' AND status = 'expired' AND reply_by >= '2026-10-20'
               AND dst = (SELECT id FROM nodes WHERE code = 'PRG-M207')
             LIMIT 500);
