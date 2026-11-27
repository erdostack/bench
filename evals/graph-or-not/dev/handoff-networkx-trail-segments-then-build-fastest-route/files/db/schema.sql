CREATE TABLE junction (
    id    TEXT PRIMARY KEY,        -- survey code, e.g. 'J0412'
    name  TEXT                     -- signpost name where there is one
);

-- One row per marked trail between two junctions. Walkable both ways. Two junctions can be joined by more
-- than one trail (a ridge path and a valley path, say); each has its own row.
CREATE TABLE segment (
    id          INTEGER PRIMARY KEY,
    junction_a  TEXT NOT NULL REFERENCES junction (id),
    junction_b  TEXT NOT NULL REFERENCES junction (id),
    trail       TEXT NOT NULL,     -- trail name or number
    length_m    INTEGER NOT NULL,
    minutes     REAL               -- surveyed walking time; NULL until the survey team has walked it
);
CREATE INDEX segment_a ON segment (junction_a);
CREATE INDEX segment_b ON segment (junction_b);
