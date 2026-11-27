-- Nightly export of the cabling spreadsheet.
CREATE TABLE device (
    name  TEXT PRIMARY KEY,                 -- 'sw03', 'dtn11'
    kind  TEXT NOT NULL CHECK (kind IN ('host', 'switch')),
    room  TEXT
);

-- One row per physical cable. Port names are in the spreadsheet, not here.
CREATE TABLE link (
    id    INTEGER PRIMARY KEY,
    a     TEXT NOT NULL REFERENCES device (name),
    b     TEXT NOT NULL REFERENCES device (name),
    gbps  REAL NOT NULL                     -- line rate of the cable
);
CREATE INDEX link_a ON link (a);
CREATE INDEX link_b ON link (b);
