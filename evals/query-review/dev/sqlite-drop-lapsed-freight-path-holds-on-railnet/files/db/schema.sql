CREATE TABLE nodes (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,          -- path, holder, route
    code    TEXT NOT NULL UNIQUE,
    name    TEXT
);
CREATE TABLE edges (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,          -- holds, runs_over
    src     INTEGER NOT NULL,
    dst     INTEGER NOT NULL,
    until   TEXT                    -- holds only: last day of the hold, YYYY-MM-DD; NULL = open-ended
);
CREATE INDEX edges_kind_until ON edges(kind, until);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
