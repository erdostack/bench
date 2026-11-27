-- Infrastructure register export (nightly). SQLite.

CREATE TABLE station (
    station_id  INTEGER PRIMARY KEY,
    crs         TEXT NOT NULL,            -- three-letter station code
    name        TEXT NOT NULL
);

-- Track nodes: points, signals, buffer stops, platform ends. A node at a station has station_id set.
CREATE TABLE track_node (
    node_id     INTEGER PRIMARY KEY,
    station_id  INTEGER REFERENCES station(station_id),
    is_core     INTEGER NOT NULL DEFAULT 0  -- 1 = on the core network (the main depots and hubs)
);

-- Track sections, usable in both directions.
CREATE TABLE section (
    section_id  INTEGER PRIMARY KEY,
    a_node      INTEGER NOT NULL REFERENCES track_node(node_id),
    b_node      INTEGER NOT NULL REFERENCES track_node(node_id)
);

CREATE INDEX section_a ON section(a_node);
CREATE INDEX section_b ON section(b_node);
