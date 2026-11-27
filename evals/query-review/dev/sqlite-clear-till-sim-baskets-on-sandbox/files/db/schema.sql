CREATE TABLE nodes (
    id          INTEGER PRIMARY KEY,
    kind        TEXT NOT NULL,
    ref         TEXT NOT NULL UNIQUE,
    source      TEXT,
    created_on  TEXT
);
CREATE INDEX nodes_kind_source ON nodes(kind, source, created_on);
CREATE TABLE edges (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    src   INTEGER NOT NULL,
    dst   INTEGER NOT NULL
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
