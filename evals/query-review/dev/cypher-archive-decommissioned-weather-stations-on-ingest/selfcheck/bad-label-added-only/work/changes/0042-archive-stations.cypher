// 0042: mark stations decommissioned before 2025 as archived
MATCH (s:Station) WHERE s.status = 'decommissioned' AND s.decommissionedOn < date('2025-01-01')
SET s:ArchivedStation;
