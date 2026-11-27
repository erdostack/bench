// Indexes behind the browse and search pages.
CREATE INDEX paper_year IF NOT EXISTS
FOR (p:Paper) ON (p.year);

CREATE INDEX author_name IF NOT EXISTS
FOR (a:Author) ON (a.name);

CREATE FULLTEXT INDEX paper_title_text IF NOT EXISTS
FOR (p:Paper) ON EACH [p.title];
