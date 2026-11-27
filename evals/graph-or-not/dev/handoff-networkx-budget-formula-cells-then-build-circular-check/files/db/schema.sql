CREATE TABLE cell (
    id       INTEGER PRIMARY KEY,
    sheet    TEXT NOT NULL,          -- 'Inputs', 'Costs', 'Loan', ...
    ref      TEXT NOT NULL,          -- 'B12'
    formula  TEXT NOT NULL,          -- '=Costs!B2*1.2' or a constant
    UNIQUE (sheet, ref)
);

-- One row per cell a formula reads. cell_id's formula mentions depends_on.
CREATE TABLE reference (
    cell_id     INTEGER NOT NULL REFERENCES cell (id),
    depends_on  INTEGER NOT NULL REFERENCES cell (id),
    PRIMARY KEY (cell_id, depends_on)
);
