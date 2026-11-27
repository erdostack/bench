CREATE TABLE station (
    id    INTEGER PRIMARY KEY,
    code  TEXT NOT NULL UNIQUE,
    kind  TEXT NOT NULL CHECK (kind IN ('station', 'dock')),
    hall  TEXT NOT NULL
);

-- A conveyor segment carries parts from from_station to to_station.
CREATE TABLE segment (
    id           INTEGER PRIMARY KEY,
    from_station INTEGER NOT NULL REFERENCES station (id),
    to_station   INTEGER NOT NULL REFERENCES station (id),
    kind         TEXT NOT NULL CHECK (kind IN ('belt', 'roller', 'bypass')),
    length_m     REAL NOT NULL
);
