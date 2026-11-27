// archive stations decommissioned before 2025 (they stay on the map otherwise); count: MATCH (s:Station {status: 'decommissioned'}) WHERE s.decommissionedOn < date('2025-01-01') RETURN count(s);
:param cutoff => '2025-01-01'
MATCH (s:Station) WHERE s.status = 'decommissioned' AND s.decommissionedOn < $cutoff
SET s:ArchivedStation REMOVE s:Station;
