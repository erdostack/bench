CREATE INDEX artist_mbid IF NOT EXISTS FOR (a:Artist) ON (a.mbid);
