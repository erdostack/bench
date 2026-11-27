CREATE TABLE zone (
    id              INTEGER PRIMARY KEY,
    parent_zone_id  INTEGER REFERENCES zone (id),   -- NULL for a site
    name            TEXT NOT NULL
);
CREATE INDEX zone_parent_idx ON zone (parent_zone_id);

CREATE TABLE door (
    id       INTEGER PRIMARY KEY,
    zone_id  INTEGER NOT NULL REFERENCES zone (id),
    label    TEXT NOT NULL
);

CREATE TABLE badge_zone (
    badge_id  INTEGER NOT NULL,
    zone_id   INTEGER NOT NULL REFERENCES zone (id),
    PRIMARY KEY (badge_id, zone_id)
);
