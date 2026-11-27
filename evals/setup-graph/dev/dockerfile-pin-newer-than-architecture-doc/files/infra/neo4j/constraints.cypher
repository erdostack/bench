CREATE CONSTRAINT release_id IF NOT EXISTS FOR (r:Release) REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT pressing_cat_no IF NOT EXISTS FOR (p:Pressing) REQUIRE p.catalogue_no IS NOT NULL;
CREATE CONSTRAINT label_name IF NOT EXISTS FOR (l:Label) REQUIRE l.name IS UNIQUE;
CREATE INDEX artist_name IF NOT EXISTS FOR (a:Artist) ON (a.name);
