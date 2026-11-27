CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- member | tool
    ref TEXT NOT NULL UNIQUE,
    name TEXT
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- loan | reservation (docs/model.md)
    src INTEGER NOT NULL REFERENCES nodes (id),
    dst INTEGER NOT NULL REFERENCES nodes (id),
    out_on TEXT NOT NULL,
    back_on TEXT
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
CREATE INDEX edges_back ON edges (kind, back_on);
CREATE TABLE loan_archive (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL,
    out_on TEXT NOT NULL,
    back_on TEXT
);
