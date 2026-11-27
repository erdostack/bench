CREATE INDEX author_orcid IF NOT EXISTS
FOR (a:Author) ON (a.orcid);
