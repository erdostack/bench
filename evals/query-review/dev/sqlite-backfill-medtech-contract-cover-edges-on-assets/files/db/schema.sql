CREATE TABLE nodes (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,          -- device, ward, vendor, contract
    code    TEXT NOT NULL UNIQUE,
    name    TEXT,
    class   TEXT,                   -- devices only
    status  TEXT                    -- devices only
);
CREATE TABLE edges (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,
    src     INTEGER NOT NULL,
    dst     INTEGER NOT NULL,
    since   TEXT
);
CREATE INDEX edges_src_kind ON edges(src, kind);
CREATE INDEX edges_dst_kind ON edges(dst, kind);
