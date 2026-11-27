// dev seed: wipe and rebuild the development graph (generated, not real stops).
MATCH (n) DETACH DELETE n;
WITH ['Hillside', 'Moorside', 'Riverside', 'Old Town', 'Westfield'] AS zones
UNWIND range(1, 1200) AS i
CREATE (:Stop {stopCode: 'DS-' + toString(i), name: 'Dev stop ' + toString(i), zone: zones[i % 5], active: true});
WITH ['Hillside', 'Moorside', 'Riverside', 'Old Town', 'Westfield'] AS zones
UNWIND range(1, 30) AS i
CREATE (:School {code: 'DSC-' + toString(i), name: 'Dev school ' + toString(i), zone: zones[i % 5]});
UNWIND ['Hillside', 'Moorside', 'Riverside'] AS z
CREATE (:Depot {name: z + ' depot', zone: z});
UNWIND range(1, 80) AS i
CREATE (r:Route {code: 'DR-' + toString(i)})
WITH r, i
MATCH (s:Stop) WHERE s.stopCode IN ['DS-' + toString(i), 'DS-' + toString(i + 80), 'DS-' + toString(i + 160), 'DS-' + toString(i + 240)]
CREATE (r)-[:CALLS_AT {seq: toInteger(split(s.stopCode, '-')[1])}]->(s);
