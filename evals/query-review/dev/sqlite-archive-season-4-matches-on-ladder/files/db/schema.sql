CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- team | player
    name TEXT NOT NULL
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,          -- match (winning team -> losing team) | plays_for (player -> team)
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL,
    season INTEGER,              -- match only
    played_at TEXT,              -- match only
    score TEXT                   -- match only, e.g. '3-1'
);
CREATE TABLE edges_archive (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL,
    season INTEGER,
    played_at TEXT,
    score TEXT
);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
CREATE INDEX edges_season ON edges (kind, season);
CREATE INDEX archive_season ON edges_archive (season);
