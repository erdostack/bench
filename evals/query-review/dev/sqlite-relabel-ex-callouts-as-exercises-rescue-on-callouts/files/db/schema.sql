CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE,
    title TEXT,
    opened_at TEXT
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL,
    role TEXT
);
CREATE INDEX nodes_kind ON nodes(kind);
