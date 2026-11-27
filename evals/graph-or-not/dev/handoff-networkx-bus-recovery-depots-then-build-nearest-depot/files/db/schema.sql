-- Road network for the control room. SQLite.

CREATE TABLE junction (
    junction_id  INTEGER PRIMARY KEY,
    name         TEXT
);

CREATE TABLE depot (
    depot_id     INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    junction_id  INTEGER NOT NULL REFERENCES junction(junction_id)
);

-- Road segments, two-way. Two segments may join the same two junctions (a bus gate beside an old road).
CREATE TABLE segment (
    segment_id  INTEGER PRIMARY KEY,
    a           INTEGER NOT NULL REFERENCES junction(junction_id),
    b           INTEGER NOT NULL REFERENCES junction(junction_id),
    minutes     REAL NOT NULL,              -- typical driving time
    bus_gate    INTEGER NOT NULL DEFAULT 0  -- 1 = buses, taxis and cycles only
);
