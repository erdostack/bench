CREATE CONSTRAINT buoy_code IF NOT EXISTS FOR (b:Buoy) REQUIRE b.code IS UNIQUE;
CREATE CONSTRAINT station_code IF NOT EXISTS FOR (s:Station) REQUIRE s.code IS UNIQUE;
UNWIND range(1, 40) AS i
MERGE (:Buoy {code: 'B' + toString(i), depth_m: 10 + (i * 7) % 90});
UNWIND ['S1', 'S2', 'S3'] AS code
MERGE (:Station {code: code});
UNWIND range(1, 39) AS i
MATCH (a:Buoy {code: 'B' + toString(i)}), (b:Buoy {code: 'B' + toString(i + 1)})
MERGE (a)-[:RELAYS_TO {range_km: 3 + i % 5}]->(b);
MATCH (b:Buoy) WHERE b.code IN ['B13', 'B26', 'B40']
MATCH (s:Station {code: 'S' + toString(toInteger(substring(b.code, 1)) / 13)})
MERGE (b)-[:RELAYS_TO {range_km: 2}]->(s);
