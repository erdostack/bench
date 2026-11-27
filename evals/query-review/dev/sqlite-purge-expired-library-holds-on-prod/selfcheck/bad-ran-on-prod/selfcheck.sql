DELETE FROM edges WHERE kind = 'hold' AND status IN ('expired', 'cancelled');
