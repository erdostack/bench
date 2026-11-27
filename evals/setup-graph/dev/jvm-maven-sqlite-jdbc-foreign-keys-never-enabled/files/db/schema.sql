CREATE TABLE substation (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    kv   INTEGER NOT NULL
);

CREATE TABLE line (
    id       INTEGER PRIMARY KEY,
    from_sub INTEGER NOT NULL REFERENCES substation(id),
    to_sub   INTEGER NOT NULL REFERENCES substation(id),
    km       REAL NOT NULL
);

CREATE INDEX line_from ON line(from_sub);
CREATE INDEX line_to ON line(to_sub);
