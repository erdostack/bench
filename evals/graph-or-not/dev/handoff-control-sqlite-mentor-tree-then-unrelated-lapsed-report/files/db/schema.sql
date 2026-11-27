CREATE TABLE volunteer (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    joined_on  TEXT NOT NULL,                 -- ISO date
    mentor_id  INTEGER REFERENCES volunteer (id),
    active     INTEGER NOT NULL DEFAULT 1     -- 0 = left the network
);
CREATE INDEX volunteer_mentor ON volunteer (mentor_id);

CREATE TABLE site (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL
);

CREATE TABLE shift (
    id            INTEGER PRIMARY KEY,
    volunteer_id  INTEGER NOT NULL REFERENCES volunteer (id),
    site_id       INTEGER NOT NULL REFERENCES site (id),
    shift_date    TEXT NOT NULL,              -- ISO date
    hours         REAL NOT NULL
);
CREATE INDEX shift_volunteer_date ON shift (volunteer_id, shift_date);
