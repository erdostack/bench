CREATE TABLE nodes (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    code  TEXT NOT NULL UNIQUE,
    name  TEXT
);
CREATE TABLE edges (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    src   INTEGER NOT NULL,
    dst   INTEGER NOT NULL,
    seq   INTEGER
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
