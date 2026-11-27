CREATE TABLE hub (
    id    INTEGER PRIMARY KEY,
    code  TEXT NOT NULL UNIQUE
);

CREATE TABLE parcel (
    id           INTEGER PRIMARY KEY,
    tracking_no  TEXT NOT NULL UNIQUE
);

-- one row per arrival scan; seq orders a parcel's scans
CREATE TABLE scan (
    id         INTEGER PRIMARY KEY,
    parcel_id  INTEGER NOT NULL REFERENCES parcel(id),
    seq        INTEGER NOT NULL,
    hub_id     INTEGER NOT NULL REFERENCES hub(id),
    at_min     INTEGER NOT NULL          -- minutes since 2026-01-01 00:00 UTC
);
CREATE INDEX scan_parcel ON scan(parcel_id, seq);

-- hub-to-hub legs derived from consecutive scans (leg_no 1 = first scan to second scan)
CREATE TABLE leg (
    id         INTEGER PRIMARY KEY,
    parcel_id  INTEGER NOT NULL REFERENCES parcel(id),
    leg_no     INTEGER NOT NULL,
    from_hub   INTEGER NOT NULL REFERENCES hub(id),
    to_hub     INTEGER NOT NULL REFERENCES hub(id),
    minutes    INTEGER NOT NULL
);
CREATE INDEX leg_parcel ON leg(parcel_id);
CREATE INDEX leg_from ON leg(from_hub);

CREATE TABLE job_progress (
    job             TEXT PRIMARY KEY,
    last_parcel_id  INTEGER NOT NULL
);
