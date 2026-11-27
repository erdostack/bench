-- Nightly timetable export (scheduling system). SQLite.

CREATE TABLE stop (
    stop_id         INTEGER PRIMARY KEY,
    code            TEXT NOT NULL,         -- the code on the flag, e.g. 'HX4021'
    name            TEXT NOT NULL,
    paired_stop_id  INTEGER REFERENCES stop(stop_id)
                    -- the stop on the other side of the road, where there is one.
                    -- The export records each pair once, on one of the two stops only.
);

CREATE TABLE route (
    route_id     INTEGER PRIMARY KEY,
    short_name   TEXT NOT NULL,            -- '12', '12A', 'X5'
    school_only  INTEGER NOT NULL DEFAULT 0
);

-- A route calls at a stop.
CREATE TABLE stop_route (
    stop_id   INTEGER NOT NULL REFERENCES stop(stop_id),
    route_id  INTEGER NOT NULL REFERENCES route(route_id),
    PRIMARY KEY (stop_id, route_id)
);
