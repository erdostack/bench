CREATE CONSTRAINT municipality_code IF NOT EXISTS FOR (m:Municipality) REQUIRE m.code IS UNIQUE;
