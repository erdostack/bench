CREATE CONSTRAINT accession_code IF NOT EXISTS FOR (b:Accession) REQUIRE b.code IS UNIQUE;
CREATE CONSTRAINT drawer_code IF NOT EXISTS FOR (d:Drawer) REQUIRE d.code IS UNIQUE;
CREATE CONSTRAINT taxon_name IF NOT EXISTS FOR (t:Taxon) REQUIRE t.name IS UNIQUE;
CREATE INDEX test_date IF NOT EXISTS FOR (g:GerminationTest) ON (g.tested_on);
