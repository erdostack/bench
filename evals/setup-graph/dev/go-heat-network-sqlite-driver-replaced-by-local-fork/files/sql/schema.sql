CREATE TABLE node (
    id   TEXT PRIMARY KEY,
    kind TEXT NOT NULL CHECK (kind IN ('plant', 'junction', 'building')),
    name TEXT NOT NULL
);

CREATE TABLE pipe (
    id        TEXT PRIMARY KEY,
    from_node TEXT NOT NULL REFERENCES node (id),
    to_node   TEXT NOT NULL REFERENCES node (id),
    dn_mm     INTEGER NOT NULL,
    length_m  REAL NOT NULL
);

CREATE INDEX pipe_from ON pipe (from_node);
CREATE INDEX pipe_to ON pipe (to_node);
