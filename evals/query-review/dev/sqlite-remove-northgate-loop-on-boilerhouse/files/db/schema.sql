CREATE TABLE nodes (
  id     INTEGER PRIMARY KEY,
  kind   TEXT NOT NULL,
  ref    TEXT NOT NULL UNIQUE,
  loop   TEXT NOT NULL,
  status TEXT NOT NULL DEFAULT 'in_service'
);
CREATE TABLE edges (
  id  INTEGER PRIMARY KEY,
  src INTEGER NOT NULL REFERENCES nodes(id),
  dst INTEGER NOT NULL REFERENCES nodes(id),
  rel TEXT NOT NULL
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
CREATE INDEX nodes_loop ON nodes(loop);
