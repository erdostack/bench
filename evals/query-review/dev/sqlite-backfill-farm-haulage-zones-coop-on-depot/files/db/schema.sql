CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    name TEXT,
    postcode TEXT,
    status TEXT
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    src INTEGER NOT NULL REFERENCES nodes(id),
    dst INTEGER NOT NULL REFERENCES nodes(id),
    since TEXT
);
CREATE INDEX edges_src ON edges(kind, src);
CREATE INDEX edges_dst ON edges(kind, dst);
CREATE TABLE zone_districts (
    district TEXT PRIMARY KEY,
    zone_code TEXT NOT NULL
);
