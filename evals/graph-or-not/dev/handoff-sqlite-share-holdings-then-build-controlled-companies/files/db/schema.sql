-- Companies and the stakes they hold in each other, as delivered by the registry feed.

CREATE TABLE company (
    id           INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    registry_no  TEXT    NOT NULL,
    country      TEXT    NOT NULL
);

-- One row per stake: owner_id holds pct percent of the shares of owned_id.
CREATE TABLE holding (
    owner_id  INTEGER NOT NULL REFERENCES company (id),
    owned_id  INTEGER NOT NULL REFERENCES company (id),
    pct       REAL    NOT NULL,
    PRIMARY KEY (owner_id, owned_id)
);
CREATE INDEX holding_owned ON holding (owned_id);

CREATE TABLE client (
    id          INTEGER PRIMARY KEY,
    company_id  INTEGER NOT NULL REFERENCES company (id),
    manager     TEXT    NOT NULL,
    onboarded   TEXT    NOT NULL
);
