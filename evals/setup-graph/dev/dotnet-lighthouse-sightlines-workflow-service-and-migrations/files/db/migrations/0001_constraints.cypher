// database: neo4j
CREATE CONSTRAINT light_code IF NOT EXISTS FOR (l:Light) REQUIRE l.code IS UNIQUE;
