CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- course | language | teacher
    ref TEXT NOT NULL UNIQUE,
    term TEXT,
    lang TEXT
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- in_language | taught_by
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
