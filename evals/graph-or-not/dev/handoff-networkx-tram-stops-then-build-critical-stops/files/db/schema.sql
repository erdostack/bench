-- Planning database, rebuilt nightly from the timetable export.
CREATE TABLE stop (
    code               TEXT PRIMARY KEY,       -- e.g. 'HBF', 'K12'
    name               TEXT NOT NULL,
    boardings_per_day  INTEGER NOT NULL DEFAULT 0
);

-- One row per pair of adjacent stops on a line. Trams run both ways, so a row is not a direction.
-- Two lines that share a stretch of track each have their own row for it.
CREATE TABLE link (
    stop_a       TEXT NOT NULL REFERENCES stop (code),
    stop_b       TEXT NOT NULL REFERENCES stop (code),
    line         TEXT NOT NULL,
    run_minutes  REAL NOT NULL
);
CREATE INDEX link_a ON link (stop_a);
CREATE INDEX link_b ON link (stop_b);
