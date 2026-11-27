CREATE TABLE docks (
    id        INTEGER PRIMARY KEY,
    code      TEXT,                     -- e.g. 'DK-0412'; backfilled by jobs/backfill_dock_codes.py
    name      TEXT NOT NULL,
    status    TEXT NOT NULL CHECK (status IN ('open', 'closed', 'planned')),
    opened_on TEXT
);

CREATE TABLE flows (
    id        INTEGER PRIMARY KEY,
    from_dock INTEGER NOT NULL REFERENCES docks(id),
    to_dock   INTEGER NOT NULL REFERENCES docks(id),
    trips     INTEGER NOT NULL DEFAULT 0,
    share     REAL,                     -- 0007
    UNIQUE (from_dock, to_dock)
);
CREATE INDEX flows_to ON flows (to_dock);
