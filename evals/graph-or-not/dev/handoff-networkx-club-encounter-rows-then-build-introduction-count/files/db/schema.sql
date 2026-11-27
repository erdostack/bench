CREATE TABLE member (
    id       INTEGER PRIMARY KEY,
    faction  TEXT NOT NULL
);

-- One row per context in which two members met (training, a class, a tournament, ...).
-- A pair that met in several contexts has several rows. member_a < member_b.
CREATE TABLE encounter (
    member_a  INTEGER NOT NULL REFERENCES member (id),
    member_b  INTEGER NOT NULL REFERENCES member (id),
    context   INTEGER NOT NULL,
    PRIMARY KEY (member_a, member_b, context)
);
