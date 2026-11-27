CREATE TABLE nodes (
    id             INTEGER PRIMARY KEY,
    kind           TEXT NOT NULL,
    code           TEXT NOT NULL UNIQUE,
    title          TEXT,
    location_code  TEXT,
    moved_on       TEXT
);
CREATE INDEX nodes_location_code ON nodes(location_code);
CREATE TABLE edges (
    id     INTEGER PRIMARY KEY,
    kind   TEXT NOT NULL,
    src    INTEGER NOT NULL,
    dst    INTEGER NOT NULL,
    since  TEXT
);
CREATE INDEX edges_src ON edges(src, kind);
CREATE INDEX edges_dst ON edges(dst);
