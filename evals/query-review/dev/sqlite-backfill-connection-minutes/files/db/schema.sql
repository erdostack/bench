CREATE TABLE stations (id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, name TEXT NOT NULL);
CREATE TABLE connections (
    id INTEGER PRIMARY KEY,
    trip_id TEXT NOT NULL,
    seq INTEGER NOT NULL,
    from_station INTEGER NOT NULL REFERENCES stations (id),
    to_station INTEGER NOT NULL REFERENCES stations (id),
    dep TEXT NOT NULL,
    arr TEXT NOT NULL,
    UNIQUE (trip_id, seq)
);
CREATE INDEX connections_from ON connections (from_station, dep);
