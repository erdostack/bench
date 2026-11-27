CREATE TABLE nodes (
    id           INTEGER PRIMARY KEY,
    kind         TEXT NOT NULL,
    code         TEXT NOT NULL UNIQUE,
    name         TEXT,
    status       TEXT,
    region_code  TEXT,
    opened_on    TEXT
);
CREATE TABLE edges (
    id     INTEGER PRIMARY KEY,
    kind   TEXT NOT NULL,
    src    INTEGER NOT NULL,
    dst    INTEGER NOT NULL,
    since  TEXT
);
CREATE INDEX edges_src_kind ON edges(src, kind);
CREATE INDEX edges_dst ON edges(dst);
