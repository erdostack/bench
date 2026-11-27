CREATE TABLE port (
    id   INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL
);

CREATE TABLE crossing (
    id        INTEGER PRIMARY KEY,
    from_port INTEGER NOT NULL,
    to_port   INTEGER NOT NULL,
    minutes   INTEGER NOT NULL
);

CREATE INDEX crossing_from ON crossing(from_port);
