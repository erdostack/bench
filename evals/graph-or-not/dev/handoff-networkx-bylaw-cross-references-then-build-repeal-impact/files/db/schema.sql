CREATE TABLE bylaw (
    id     INTEGER PRIMARY KEY,
    title  TEXT NOT NULL,
    year   INTEGER NOT NULL
);

-- from_bylaw's text refers to to_bylaw.
CREATE TABLE reference (
    from_bylaw  INTEGER NOT NULL REFERENCES bylaw (id),
    to_bylaw    INTEGER NOT NULL REFERENCES bylaw (id),
    kind        TEXT NOT NULL CHECK (kind IN ('amends', 'depends_on', 'cites')),
    PRIMARY KEY (from_bylaw, to_bylaw, kind)
);
CREATE INDEX reference_to ON reference (to_bylaw);
