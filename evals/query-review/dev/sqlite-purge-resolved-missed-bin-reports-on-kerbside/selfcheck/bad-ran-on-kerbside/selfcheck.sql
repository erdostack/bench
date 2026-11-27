DELETE FROM edges WHERE kind = 'missed' AND status = 'resolved' AND reported_on < '2026-10-01';
