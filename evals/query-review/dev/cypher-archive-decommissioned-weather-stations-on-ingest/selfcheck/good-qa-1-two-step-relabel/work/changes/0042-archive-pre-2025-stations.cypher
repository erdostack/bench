// 0042: archive in two steps
MATCH (s:Station)
WHERE s.status = 'decommissioned' AND s.decommissionedOn < date('2025-01-01')
SET s:ArchivedStation;
MATCH (s:Station:ArchivedStation)
REMOVE s:Station;
