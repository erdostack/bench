DELETE FROM models WHERE id IN (
  SELECT m.id FROM models m
  LEFT JOIN antennas a ON a.model_id = m.id
  LEFT JOIN spares s ON s.model_code = m.code
  WHERE m.status = 'retired'
  GROUP BY m.id
  HAVING count(a.id) = 0 AND count(s.id) = 0
);
