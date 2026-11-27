CREATE TABLE researcher (
    id        INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    phd_year  INTEGER
);

-- Who advised whose dissertation. Co-advised dissertations have two rows.
CREATE TABLE advising (
    student_id  INTEGER NOT NULL REFERENCES researcher (id),
    advisor_id  INTEGER NOT NULL REFERENCES researcher (id),
    role        TEXT NOT NULL DEFAULT 'advisor',   -- 'advisor' or 'co-advisor'
    PRIMARY KEY (student_id, advisor_id)
);
CREATE INDEX advising_student ON advising (student_id);
