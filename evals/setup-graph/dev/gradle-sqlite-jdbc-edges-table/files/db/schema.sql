CREATE TABLE junction (
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE link (
    from_id INTEGER NOT NULL REFERENCES junction (id),
    to_id   INTEGER NOT NULL REFERENCES junction (id),
    km      REAL    NOT NULL CHECK (km > 0),
    PRIMARY KEY (from_id, to_id)
);

CREATE INDEX link_to ON link (to_id);
