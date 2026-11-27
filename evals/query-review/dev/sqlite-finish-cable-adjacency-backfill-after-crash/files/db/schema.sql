CREATE TABLE sites (
  id INTEGER PRIMARY KEY,
  code TEXT NOT NULL UNIQUE,
  kind TEXT NOT NULL              -- exchange | cabinet | chamber
);
CREATE TABLE cables (
  id INTEGER PRIMARY KEY,
  a_site INTEGER NOT NULL REFERENCES sites(id),
  b_site INTEGER NOT NULL REFERENCES sites(id),
  fibres INTEGER NOT NULL,
  status TEXT NOT NULL            -- in_service | planned | recovered
);
-- Edges the route planner walks. Two kinds of row:
--   origin 'cable'  : one per in-service cable, written by jobs/build_adjacency.py
--   origin 'survey' : duct routes recorded by field survey crews (no cable yet; cable_id is NULL),
--                     loaded by the survey importer. The adjacency job never touches these.
CREATE TABLE adjacency (
  id INTEGER PRIMARY KEY,
  src INTEGER NOT NULL REFERENCES sites(id),
  dst INTEGER NOT NULL REFERENCES sites(id),
  cable_id INTEGER REFERENCES cables(id),
  origin TEXT NOT NULL
);
CREATE INDEX adjacency_src ON adjacency(src);
