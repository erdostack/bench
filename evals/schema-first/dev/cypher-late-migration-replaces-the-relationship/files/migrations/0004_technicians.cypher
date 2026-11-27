CREATE CONSTRAINT technician_badge IF NOT EXISTS FOR (t:Technician) REQUIRE t.badge IS UNIQUE;
