CREATE TABLE drug_class (
    id    INTEGER PRIMARY KEY,
    code  TEXT NOT NULL UNIQUE,
    name  TEXT NOT NULL
);

CREATE TABLE drug (
    id        INTEGER PRIMARY KEY,
    name      TEXT    NOT NULL,
    class_id  INTEGER NOT NULL REFERENCES drug_class (id)
);
CREATE INDEX drug_class_idx ON drug (class_id);

-- A rule names two sides; each side is either a drug or a class (exactly one of the pair is set).
CREATE TABLE interaction_rule (
    id          INTEGER PRIMARY KEY,
    a_drug_id   INTEGER REFERENCES drug (id),
    a_class_id  INTEGER REFERENCES drug_class (id),
    b_drug_id   INTEGER REFERENCES drug (id),
    b_class_id  INTEGER REFERENCES drug_class (id),
    severity    TEXT    NOT NULL CHECK (severity IN ('minor', 'moderate', 'major', 'contraindicated')),
    advice      TEXT    NOT NULL
);

CREATE TABLE patient_medication (
    patient_id  INTEGER NOT NULL,
    drug_id     INTEGER NOT NULL REFERENCES drug (id),
    started     DATE    NOT NULL,
    stopped     DATE
);
