// 0042: archive decommissioned stations closed before 2025, in two passes (before 2020, then 2020-2024).
MATCH (s:Station {status: 'decommissioned'}) WHERE s.decommissionedOn.year < 2020
SET s:ArchivedStation REMOVE s:Station;
MATCH (s:Station {status: 'decommissioned'}) WHERE 2020 <= s.decommissionedOn.year <= 2024
SET s:ArchivedStation REMOVE s:Station;
