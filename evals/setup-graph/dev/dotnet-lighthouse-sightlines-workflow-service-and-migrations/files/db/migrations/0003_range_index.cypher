// database: neo4j
CREATE RANGE INDEX light_range IF NOT EXISTS FOR (l:Light) ON (l.range_nm);
