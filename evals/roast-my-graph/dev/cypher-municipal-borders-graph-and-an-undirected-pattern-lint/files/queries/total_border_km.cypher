// the undirected match sees every border from both ends, so halve the sum
MATCH (:Municipality)-[r:BORDERS]-(:Municipality)
RETURN sum(r.length_km) / 2 AS internal_border_km;
