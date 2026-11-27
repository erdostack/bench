CREATE TABLE junction (
    id      INTEGER PRIMARY KEY,     -- 1 is the gritting depot
    houses  INTEGER NOT NULL DEFAULT 0
);

-- One row per road segment between two junctions. Two different roads can join the same two junctions.
CREATE TABLE segment (
    id  INTEGER PRIMARY KEY,
    a   INTEGER NOT NULL REFERENCES junction (id),
    b   INTEGER NOT NULL REFERENCES junction (id)
);
