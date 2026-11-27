CREATE TABLE bed (
    code TEXT PRIMARY KEY,
    house TEXT NOT NULL
);

CREATE TABLE specimen (
    id TEXT PRIMARY KEY,
    taxon TEXT NOT NULL,
    bed_code TEXT REFERENCES bed(code),
    parent_id TEXT REFERENCES specimen(id),
    method TEXT CHECK (method IN ('accession', 'cutting', 'division', 'graft', 'seed'))
);

CREATE TABLE label (
    bed_code TEXT NOT NULL REFERENCES bed(code),
    taxon TEXT NOT NULL,
    printed_on TEXT
);
