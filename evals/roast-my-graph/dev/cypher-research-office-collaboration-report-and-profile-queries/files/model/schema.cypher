CREATE CONSTRAINT researcher_id IF NOT EXISTS FOR (r:Researcher) REQUIRE r.id IS UNIQUE;
CREATE INDEX researcher_institute IF NOT EXISTS FOR (r:Researcher) ON (r.institute);
