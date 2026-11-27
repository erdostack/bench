CREATE TABLE devices (
    id       INTEGER PRIMARY KEY,
    serial   TEXT NOT NULL UNIQUE,
    kind     TEXT NOT NULL CHECK (kind IN ('gateway', 'sensor')),
    customer TEXT
);

CREATE TABLE rings (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL UNIQUE,
    member_count  INTEGER NOT NULL DEFAULT 0
);

-- device belongs to ring (one ring per device)
CREATE TABLE ring_members (
    device   INTEGER PRIMARY KEY REFERENCES devices(id),
    ring_id  INTEGER NOT NULL REFERENCES rings(id)
);
CREATE INDEX ring_members_ring ON ring_members (ring_id);
