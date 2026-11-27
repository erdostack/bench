-- Timetable and performance export. SQLite.

CREATE TABLE station (
    station_code  TEXT PRIMARY KEY,     -- three letters
    name          TEXT NOT NULL
);

CREATE TABLE line (
    line_id  INTEGER PRIMARY KEY,
    name     TEXT NOT NULL
);

-- A line calls at a station.
CREATE TABLE line_station (
    line_id       INTEGER NOT NULL REFERENCES line(line_id),
    station_code  TEXT NOT NULL REFERENCES station(station_code),
    PRIMARY KEY (line_id, station_code)
);

-- One row per timetabled departure of a service from a station. Times are local, 'YYYY-MM-DDTHH:MM'.
-- actual is NULL when the train did not run from that station (cancelled or terminated short).
CREATE TABLE departure (
    service_id    TEXT NOT NULL,
    station_code  TEXT NOT NULL REFERENCES station(station_code),
    scheduled     TEXT NOT NULL,
    actual        TEXT,
    PRIMARY KEY (service_id, station_code)
);
