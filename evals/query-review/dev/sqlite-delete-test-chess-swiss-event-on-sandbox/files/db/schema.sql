CREATE TABLE nodes (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,
    code    TEXT NOT NULL UNIQUE,
    name    TEXT,
    status  TEXT
);
CREATE TABLE edges (
    id      INTEGER PRIMARY KEY,
    kind    TEXT NOT NULL,
    src     INTEGER NOT NULL,
    dst     INTEGER NOT NULL,
    event   INTEGER,
    round   INTEGER,
    result  TEXT
);
CREATE INDEX edges_src ON edges(src);
CREATE INDEX edges_dst ON edges(dst);
CREATE INDEX edges_event ON edges(event);
