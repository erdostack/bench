DELETE FROM edges WHERE kind = 'held' AND held_until < datetime('now');
