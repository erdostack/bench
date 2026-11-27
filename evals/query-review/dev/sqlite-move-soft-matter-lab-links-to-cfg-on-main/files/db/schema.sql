CREATE TABLE nodes (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    key   TEXT NOT NULL UNIQUE,
    name  TEXT
);
CREATE TABLE edges (
    id   INTEGER PRIMARY KEY,
    rel  TEXT NOT NULL,
    src  INTEGER NOT NULL,
    dst  INTEGER NOT NULL
);
CREATE UNIQUE INDEX edges_unique ON edges(rel, src, dst);
CREATE INDEX edges_dst ON edges(dst, rel);
