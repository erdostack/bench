CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- reservoir | backpump | pound
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- pumps_to | feeds | standby_for
    src INTEGER NOT NULL REFERENCES nodes (id),
    dst INTEGER NOT NULL REFERENCES nodes (id)
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
