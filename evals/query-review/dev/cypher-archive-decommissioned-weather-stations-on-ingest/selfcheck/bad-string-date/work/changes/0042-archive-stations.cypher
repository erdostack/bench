// 0042: archive stations decommissioned before 2025
MATCH (s:Station) WHERE s.status = 'decommissioned' AND s.decommissionedOn < '2025-01-01'
SET s:ArchivedStation REMOVE s:Station;
