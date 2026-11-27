CREATE TABLE member (
    id       INTEGER PRIMARY KEY,
    faction  TEXT NOT NULL
);

CREATE TABLE tie (
    a         INTEGER NOT NULL REFERENCES member (id),
    b         INTEGER NOT NULL REFERENCES member (id),
    contexts  INTEGER NOT NULL,
    PRIMARY KEY (a, b)
);
