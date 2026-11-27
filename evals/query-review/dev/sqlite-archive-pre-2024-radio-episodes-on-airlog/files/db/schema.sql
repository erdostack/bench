CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- show | presenter | track | episode
    ref TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    aired_on TEXT                  -- episodes only: YYYY-MM-DD, NULL for a pilot never broadcast
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- episode_of | hosted_by | played | repeat_of (docs/model.md)
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL
);
CREATE TABLE nodes_archive (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    ref TEXT NOT NULL,
    title TEXT NOT NULL,
    aired_on TEXT
);
CREATE TABLE edges_archive (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL
);
CREATE INDEX nodes_kind_aired ON nodes (kind, aired_on);
CREATE INDEX edges_src ON edges (src, kind);
CREATE INDEX edges_dst ON edges (dst, kind);
