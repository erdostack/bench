CREATE TABLE node (
  id   INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,
  code TEXT NOT NULL UNIQUE,
  name TEXT
);
CREATE TABLE edge (
  src   INTEGER NOT NULL,
  dst   INTEGER NOT NULL,
  rel   TEXT NOT NULL,
  route TEXT NOT NULL DEFAULT '',
  PRIMARY KEY (src, dst, rel, route)
);
CREATE INDEX edge_dst ON edge(dst);
CREATE TABLE stop_merge (
  dup_id  INTEGER PRIMARY KEY,
  keep_id INTEGER NOT NULL
);
