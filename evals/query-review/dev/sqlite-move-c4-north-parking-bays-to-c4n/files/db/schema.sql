CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    ref TEXT NOT NULL,
    street TEXT,
    sector TEXT
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    src INTEGER NOT NULL REFERENCES nodes(id),
    dst INTEGER NOT NULL REFERENCES nodes(id)
);
CREATE INDEX edges_kind_dst ON edges(kind, dst);
CREATE INDEX edges_src ON edges(src);
