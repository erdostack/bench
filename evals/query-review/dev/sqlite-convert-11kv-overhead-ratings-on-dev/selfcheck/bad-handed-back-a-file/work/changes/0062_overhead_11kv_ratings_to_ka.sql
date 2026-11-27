UPDATE edges SET rating = rating / 1000.0, rating_unit = 'kA' WHERE kind = 'overhead_line' AND voltage_kv = 11 AND rating_unit = 'A';
