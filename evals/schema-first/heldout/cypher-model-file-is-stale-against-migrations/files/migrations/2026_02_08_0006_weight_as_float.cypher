MATCH (s:Shipment) WHERE s.weightKg IS NOT NULL
SET s.weightKg = toFloat(s.weightKg);
