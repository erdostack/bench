CREATE TABLE variant (
    id    INTEGER PRIMARY KEY,
    code  TEXT NOT NULL UNIQUE          -- 'CITY-48V-L', ...
);

-- Connector pins and splice points. Everything a wire can end at.
CREATE TABLE endpoint (
    id          BIGINT PRIMARY KEY,
    variant_id  INTEGER NOT NULL REFERENCES variant (id),
    connector   TEXT NOT NULL,          -- 'X12', 'SP4' for a splice
    pin         TEXT
);

CREATE TABLE wire (
    id          BIGINT PRIMARY KEY,
    variant_id  INTEGER NOT NULL REFERENCES variant (id),
    from_ep     BIGINT NOT NULL REFERENCES endpoint (id),
    to_ep       BIGINT NOT NULL REFERENCES endpoint (id),
    gauge_mm2   REAL NOT NULL,
    colour      TEXT NOT NULL
);
CREATE INDEX wire_from ON wire (from_ep);
CREATE INDEX wire_to ON wire (to_ep);
