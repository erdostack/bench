CREATE TABLE junctions (
    id   INTEGER PRIMARY KEY,
    ref  TEXT NOT NULL,          -- survey reference, e.g. 'JN-0004711'
    lat  REAL NOT NULL,
    lon  REAL NOT NULL
);
-- The ops search box looks refs up case-insensitively.
CREATE INDEX junctions_ref_ci ON junctions(ref COLLATE NOCASE);

CREATE TABLE segments (
    id        INTEGER PRIMARY KEY,
    from_ref  TEXT NOT NULL,
    to_ref    TEXT NOT NULL,
    length_m  REAL NOT NULL,
    road_class TEXT NOT NULL
);
