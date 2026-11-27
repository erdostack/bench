// 0042: archive stations decommissioned before 2025
MATCH (s:Station) WHERE s.status = 'decommissioned' AND s.decommissionedOn < datetime('2025-01-01T00:00:00Z')
SET s:ArchivedStation REMOVE s:Station;
