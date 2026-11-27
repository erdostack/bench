CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- performance | patron | staff
    ref TEXT NOT NULL UNIQUE,
    name TEXT,
    starts_at TEXT
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- booked | held
    src INTEGER NOT NULL REFERENCES nodes (id),
    dst INTEGER NOT NULL REFERENCES nodes (id),
    seat TEXT NOT NULL,
    created_at TEXT NOT NULL
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
