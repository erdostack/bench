CREATE TABLE headings (
    id       INTEGER PRIMARY KEY,
    heading  TEXT NOT NULL UNIQUE
);

CREATE TABLE see_also (
    a         INTEGER NOT NULL REFERENCES headings(id),
    b         INTEGER NOT NULL REFERENCES headings(id),
    added_by  TEXT NOT NULL,
    added_at  TEXT NOT NULL
);
CREATE INDEX see_also_a ON see_also (a);
