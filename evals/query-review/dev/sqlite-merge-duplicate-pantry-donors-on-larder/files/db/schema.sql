CREATE TABLE nodes (
    id           INTEGER PRIMARY KEY,
    kind         TEXT NOT NULL,
    ref          TEXT NOT NULL UNIQUE,
    name         TEXT,
    postcode     TEXT,
    merged_into  INTEGER
);
CREATE INDEX nodes_kind ON nodes(kind);
CREATE INDEX nodes_merged ON nodes(merged_into);
CREATE TABLE edges (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    src   INTEGER NOT NULL,
    dst   INTEGER NOT NULL,
    qty   INTEGER,
    at    TEXT
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
