CREATE TABLE family (name TEXT PRIMARY KEY);

-- One row per pair of families joined by marriage. Undirected; each pair once.
CREATE TABLE marriage (
    family_a  TEXT NOT NULL REFERENCES family (name),
    family_b  TEXT NOT NULL REFERENCES family (name),
    PRIMARY KEY (family_a, family_b)
);
