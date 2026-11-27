CREATE TABLE character (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE tie (
    a         INTEGER NOT NULL REFERENCES character (id),
    b         INTEGER NOT NULL REFERENCES character (id),
    chapters  INTEGER NOT NULL,
    PRIMARY KEY (a, b)
);
