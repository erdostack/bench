CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- track | artist | release | rotation
    ref TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    import_batch TEXT              -- the import that created the row (docs/imports.md); NULL for hand entries
);
CREATE TABLE edges (
    id INTEGER PRIMARY KEY,
    kind TEXT NOT NULL,            -- by_artist (track -> artist) | on_release (track -> release) | in_rotation (track -> rotation)
    src INTEGER NOT NULL,
    dst INTEGER NOT NULL
);
CREATE INDEX nodes_batch ON nodes (import_batch);
CREATE INDEX edges_src ON edges (src);
CREATE INDEX edges_dst ON edges (dst);
