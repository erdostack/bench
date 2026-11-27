CREATE CONSTRAINT researcher_orcid IF NOT EXISTS FOR (r:Researcher) REQUIRE r.orcid IS UNIQUE;
