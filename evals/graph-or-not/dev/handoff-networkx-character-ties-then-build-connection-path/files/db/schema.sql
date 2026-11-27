CREATE TABLE character (
    id    TEXT PRIMARY KEY,      -- 'Valjean', 'MmeThenardier', ...
    name  TEXT NOT NULL
);

-- One row per pair of characters who appear together in at least one chapter. Undirected: each pair once.
CREATE TABLE tie (
    char_a  TEXT NOT NULL REFERENCES character (id),
    char_b  TEXT NOT NULL REFERENCES character (id),
    weight  INTEGER NOT NULL,     -- number of chapters in which both appear
    PRIMARY KEY (char_a, char_b)
);
CREATE INDEX tie_b ON tie (char_b);
