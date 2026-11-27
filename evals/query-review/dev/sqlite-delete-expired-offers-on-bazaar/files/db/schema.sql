CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- player | item
    name TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- owns | listed | offer (docs/trading.md)
    src INTEGER NOT NULL REFERENCES nodes (id),
    dst INTEGER NOT NULL REFERENCES nodes (id),
    status TEXT,
    price INTEGER,
    created_at TEXT NOT NULL,
    expires_at TEXT
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
CREATE INDEX edges_kind_status ON edges (kind, status, expires_at);
