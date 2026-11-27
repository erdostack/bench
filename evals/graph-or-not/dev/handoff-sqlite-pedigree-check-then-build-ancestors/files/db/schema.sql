-- Herd book. Portable DDL: runs on Postgres 15 and on SQLite (tests).
CREATE TABLE animal (
    id        INTEGER PRIMARY KEY,
    tag       TEXT NOT NULL UNIQUE,
    sex       TEXT NOT NULL CHECK (sex IN ('M', 'F')),
    born_on   DATE,
    sire_id   INTEGER REFERENCES animal (id),   -- father; NULL for founders
    dam_id    INTEGER REFERENCES animal (id)    -- mother; NULL for founders
);
CREATE INDEX animal_sire_idx ON animal (sire_id);
CREATE INDEX animal_dam_idx ON animal (dam_id);

CREATE TABLE mating (
    id            INTEGER PRIMARY KEY,
    sire_id       INTEGER NOT NULL REFERENCES animal (id),
    dam_id        INTEGER NOT NULL REFERENCES animal (id),
    submitted_on  DATE NOT NULL,
    status        TEXT NOT NULL DEFAULT 'pending'   -- pending, registered, refused
);
