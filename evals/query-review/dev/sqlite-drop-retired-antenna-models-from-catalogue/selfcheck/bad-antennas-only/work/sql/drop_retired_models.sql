DELETE FROM models WHERE status = 'retired' AND id NOT IN (SELECT model_id FROM antennas);
