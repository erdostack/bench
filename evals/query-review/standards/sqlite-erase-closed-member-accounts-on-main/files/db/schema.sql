CREATE TABLE nodes (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,      -- person | wall | group | post | comment | tag | city
    name    TEXT NOT NULL,
    created TEXT NOT NULL
);
CREATE TABLE edges (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,      -- see docs/graph.md
    src     INTEGER NOT NULL,
    dst     INTEGER NOT NULL,
    created TEXT
);
CREATE INDEX nodes_kind ON nodes (kind);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
