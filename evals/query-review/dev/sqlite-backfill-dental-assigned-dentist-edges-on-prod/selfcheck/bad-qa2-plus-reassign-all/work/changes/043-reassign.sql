-- ticket: x
UPDATE edges SET dst = (SELECT l.dst FROM edges r JOIN edges l ON l.src = r.dst AND l.kind = 'lead_dentist' WHERE r.src = edges.src AND r.kind = 'registered_at') WHERE id IN (SELECT id FROM edges WHERE kind = 'assigned_to' AND dst <> (SELECT l.dst FROM edges r JOIN edges l ON l.src = r.dst AND l.kind = 'lead_dentist' WHERE r.src = edges.src AND r.kind = 'registered_at') LIMIT 400);
