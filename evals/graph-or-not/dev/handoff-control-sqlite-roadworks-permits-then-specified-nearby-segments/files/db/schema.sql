-- Street network from the gazetteer (weekly). SQLite.

CREATE TABLE junction (
    junction_id  INTEGER PRIMARY KEY
);

CREATE TABLE segment (
    segment_id  INTEGER PRIMARY KEY,
    street      TEXT NOT NULL,
    j1          INTEGER NOT NULL REFERENCES junction(junction_id),
    j2          INTEGER NOT NULL REFERENCES junction(junction_id)
);

CREATE INDEX segment_j1 ON segment(j1);
CREATE INDEX segment_j2 ON segment(j2);

-- Bus routes using a segment.
CREATE TABLE segment_route (
    segment_id  INTEGER NOT NULL REFERENCES segment(segment_id),
    operator    TEXT NOT NULL,
    route       TEXT NOT NULL
);
