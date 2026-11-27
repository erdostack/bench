// 0042: archive stations out of service before 2025
MATCH (s:Station) WHERE s.status <> 'active' AND (s.decommissionedOn IS NULL OR s.decommissionedOn < date('2025-01-01'))
SET s:ArchivedStation REMOVE s:Station;
