DELETE FROM edges WHERE kind = 'trial' AND status IN ('no_show', 'cancelled') AND lesson_on < '2026-01-01';
