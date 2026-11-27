CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- team | pitch | referee | fixture
    code TEXT NOT NULL UNIQUE,
    name TEXT,
    kickoff TEXT                   -- fixtures only: 'YYYY-MM-DD HH:MM'
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- home | away | played_at | refereed_by
    src INTEGER NOT NULL REFERENCES nodes (id),
    dst INTEGER NOT NULL REFERENCES nodes (id)
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
