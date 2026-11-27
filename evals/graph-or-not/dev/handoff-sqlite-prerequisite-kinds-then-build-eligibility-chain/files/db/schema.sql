CREATE TABLE course (
    id     INTEGER PRIMARY KEY,
    code   TEXT NOT NULL UNIQUE,      -- e.g. 'CHEM 210'
    title  TEXT NOT NULL,
    level  INTEGER NOT NULL           -- 100, 200, 300, 400
);

-- As exported by the registrar: one row per prerequisite listed in the catalogue entry of course_id.
-- kind is 'required', 'concurrent' (may be taken in the same term) or 'recommended'.
CREATE TABLE prerequisite (
    course_id    INTEGER NOT NULL REFERENCES course (id),
    requires_id  INTEGER NOT NULL REFERENCES course (id),
    kind         TEXT NOT NULL,
    PRIMARY KEY (course_id, requires_id)
);
CREATE INDEX prerequisite_requires ON prerequisite (requires_id);
