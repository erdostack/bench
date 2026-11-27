// 013: delete the Tree nodes felled before 2024-01-01 (status 'felled' and felledOn < 2024-01-01), with their
// relationships, so the public tree map stops drawing them as grey dots. Requested by the map's maintainer.
// Expect about 7,800 trees (docs/model.md). Count before (and again after, which must give 0):
//   MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn < date('2024-01-01') RETURN count(t);
// Also check, before: MATCH (t:Tree {status: 'felled'}) WHERE t.felledOn IS NULL RETURN count(t);
//   those have no felled date, are not matched by this file, and stay on the map.
// Limit (docs/changes.md): at most 5,000 nodes and relationships together per transaction. A tree is at most
// 1 node + 43 relationships (docs/model.md), 44 in all, so 100 trees per transaction is at most 4,400.
// Relationships to the street, ward, species and surveyors, and REPLACED_BY links, go with each tree; the
// Street, Ward, Species and Surveyor nodes stay. A felled tree's replacement tree stays, minus its REPLACED_BY link.
// Written for Neo4j 5.26 (CALL (t) { } scope clause needs 5.23+), not run: no copy of canopy exists
// (docs/environments.md). Check the syntax with EXPLAIN on canopy (plan only) before the real run.
// Re-running is safe: trees already deleted no longer match, so a stopped run carries on with the rest.
// Question for the reviewer: should felled trees that still have a REPLACED_BY link to a standing tree go?
// This file removes them, as the request says.
MATCH (t:Tree {status: 'felled'})
WHERE t.felledOn < date('2024-01-01')
CALL (t) {
  DETACH DELETE t
} IN TRANSACTIONS OF 100 ROWS;
