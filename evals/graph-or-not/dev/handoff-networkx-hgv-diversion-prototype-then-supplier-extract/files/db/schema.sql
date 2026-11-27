-- Road network (supplier extract). SQLite.

CREATE TABLE junction (
    junction_id  INTEGER PRIMARY KEY,
    x            REAL NOT NULL,
    y            REAL NOT NULL
);

CREATE TABLE segment (
    segment_id    INTEGER PRIMARY KEY,
    from_j        INTEGER NOT NULL REFERENCES junction(junction_id),
    to_j          INTEGER NOT NULL REFERENCES junction(junction_id),
    minutes       REAL NOT NULL,           -- free-flow travel time
    max_weight_t  REAL,                    -- weight restriction in tonnes; NULL = none
    oneway        INTEGER NOT NULL DEFAULT 0   -- 1 = only from_j -> to_j
);
