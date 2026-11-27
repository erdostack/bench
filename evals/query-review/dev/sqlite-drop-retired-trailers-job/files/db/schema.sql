CREATE TABLE tractor (
    id       INTEGER PRIMARY KEY,
    unit_no  TEXT NOT NULL UNIQUE
);

CREATE TABLE trailer (
    id          INTEGER PRIMARY KEY,
    trailer_no  TEXT NOT NULL UNIQUE,
    kind        TEXT NOT NULL CHECK (kind IN ('dry', 'reefer', 'flatbed')),
    status      TEXT NOT NULL CHECK (status IN ('in_service', 'shop', 'retired')),
    retired_on  TEXT
);

CREATE TABLE chassis (
    id          INTEGER PRIMARY KEY,
    chassis_no  TEXT NOT NULL UNIQUE
);

-- tractor pulled trailer
CREATE TABLE coupling (
    id          INTEGER PRIMARY KEY,
    tractor_id  INTEGER NOT NULL REFERENCES tractor(id),
    trailer_id  INTEGER NOT NULL REFERENCES trailer(id),
    coupled_at  TEXT NOT NULL
);
CREATE INDEX coupling_trailer ON coupling(trailer_id);

CREATE TABLE inspection (
    id            INTEGER PRIMARY KEY,
    asset_no      TEXT NOT NULL,      -- trailer_no or chassis_no (vendor feed)
    inspected_on  TEXT NOT NULL,
    result        TEXT NOT NULL CHECK (result IN ('pass', 'fail', 'conditional'))
);
CREATE INDEX inspection_asset ON inspection(asset_no);
