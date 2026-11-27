CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- fixture | store | staff | van_route
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    status TEXT                  -- fixture: in_stock | on_hire | in_repair; store: open | closing
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- stored_at | works_at | serves
    src INTEGER NOT NULL REFERENCES nodes (id),
    dst INTEGER NOT NULL REFERENCES nodes (id)
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
