CREATE TABLE family (name TEXT PRIMARY KEY);

-- One row per marriage tie between two families. Undirected; each pair once, family_a < family_b.
CREATE TABLE marriage_tie (
    family_a  TEXT NOT NULL REFERENCES family (name),
    family_b  TEXT NOT NULL REFERENCES family (name),
    PRIMARY KEY (family_a, family_b)
);
