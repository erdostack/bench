CREATE CONSTRAINT step_uid IF NOT EXISTS FOR (s:Step) REQUIRE s.uid IS UNIQUE;
CREATE CONSTRAINT procedure_version IF NOT EXISTS FOR (p:Procedure) REQUIRE (p.id, p.version) IS UNIQUE;
