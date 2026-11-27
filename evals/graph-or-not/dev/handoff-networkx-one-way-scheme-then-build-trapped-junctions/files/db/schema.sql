-- One draft one-way scheme. SQLite.

CREATE TABLE junction (
    junction_id  INTEGER PRIMARY KEY,
    name         TEXT,
    on_ring      INTEGER NOT NULL DEFAULT 0   -- 1 = on the ring road (two-way all round)
);

CREATE TABLE segment (
    segment_id  INTEGER PRIMARY KEY,
    a           INTEGER NOT NULL REFERENCES junction(junction_id),
    b           INTEGER NOT NULL REFERENCES junction(junction_id),
    oneway      INTEGER NOT NULL DEFAULT 0,   -- 0 two-way; 1 only a -> b; -1 only b -> a
    mode        TEXT NOT NULL DEFAULT 'road'  -- 'road' or 'foot'
);
