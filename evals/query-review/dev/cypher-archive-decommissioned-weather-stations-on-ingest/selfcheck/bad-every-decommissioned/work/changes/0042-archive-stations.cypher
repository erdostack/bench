// 0042: archive decommissioned stations
MATCH (s:Station {status: 'decommissioned'}) SET s:ArchivedStation REMOVE s:Station;
