CREATE TABLE location (
    id    INTEGER PRIMARY KEY,
    code  TEXT NOT NULL UNIQUE,      -- e.g. A-03-12
    zone  TEXT NOT NULL,
    kind  TEXT NOT NULL CHECK (kind IN ('bin', 'aisle_end', 'staging', 'dock'))
);

CREATE TABLE pick_edge (
    id          INTEGER PRIMARY KEY,
    from_loc    INTEGER NOT NULL REFERENCES location(id),
    to_loc      INTEGER NOT NULL REFERENCES location(id),
    metres      REAL NOT NULL,
    source      TEXT NOT NULL CHECK (source IN ('survey', 'manual', 'sim')),
    adopted_on  TEXT
);
CREATE INDEX pick_edge_from ON pick_edge(from_loc);
CREATE INDEX pick_edge_to ON pick_edge(to_loc);
