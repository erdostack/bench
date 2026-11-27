CREATE TABLE ports (
    id      INTEGER PRIMARY KEY,
    locode  TEXT NOT NULL UNIQUE,
    name    TEXT NOT NULL
);

CREATE TABLE box_legs (
    id             INTEGER PRIMARY KEY,
    container      TEXT NOT NULL,
    origin         INTEGER NOT NULL REFERENCES ports(id),
    dest           INTEGER NOT NULL REFERENCES ports(id),
    discharged_on  TEXT NOT NULL          -- YYYY-MM-DD
);
CREATE INDEX box_legs_day ON box_legs (discharged_on);

-- all-time number of boxes carried origin -> dest
CREATE TABLE lanes (
    origin  INTEGER NOT NULL REFERENCES ports(id),
    dest    INTEGER NOT NULL REFERENCES ports(id),
    boxes   INTEGER NOT NULL,
    PRIMARY KEY (origin, dest)
) WITHOUT ROWID;

-- days whose box legs have been added to lanes
CREATE TABLE lane_days (
    day   TEXT PRIMARY KEY,
    legs  INTEGER NOT NULL
);
