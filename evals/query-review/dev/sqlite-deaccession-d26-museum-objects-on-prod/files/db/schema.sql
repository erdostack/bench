CREATE TABLE nodes (
    id              INTEGER PRIMARY KEY,
    kind            TEXT NOT NULL,
    code            TEXT NOT NULL UNIQUE,
    title           TEXT,
    status          TEXT,
    disposal_batch  TEXT,
    legal_hold      INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX nodes_batch ON nodes(disposal_batch);
CREATE TABLE edges (
    id    INTEGER PRIMARY KEY,
    kind  TEXT NOT NULL,
    src   INTEGER NOT NULL,
    dst   INTEGER NOT NULL
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
