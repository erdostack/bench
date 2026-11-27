CREATE TABLE woman (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE event (
    id     INTEGER PRIMARY KEY,
    label  TEXT NOT NULL UNIQUE      -- 'E1' .. 'E14', in date order
);

CREATE TABLE attended (
    woman_id  INTEGER NOT NULL REFERENCES woman (id),
    event_id  INTEGER NOT NULL REFERENCES event (id),
    PRIMARY KEY (woman_id, event_id)
);
