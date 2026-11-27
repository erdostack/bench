// 0042: archive the stations decommissioned before 2025 (412): ArchivedStation instead of Station, so they
// leave the forecasters' map and the API. Properties and relationships stay (docs/model.md).
MATCH (s:Station)
WHERE s.status = 'decommissioned' AND s.decommissionedOn < date('2025-01-01')
SET s:ArchivedStation
REMOVE s:Station;
