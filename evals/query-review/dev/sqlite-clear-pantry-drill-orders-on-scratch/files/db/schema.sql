CREATE TABLE nodes (
    id       INTEGER PRIMARY KEY,
    kind     TEXT NOT NULL,
    ref      TEXT NOT NULL UNIQUE,
    status   TEXT,
    created  TEXT
);
CREATE TABLE edges (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    src   INTEGER NOT NULL,
    dst   INTEGER NOT NULL
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
