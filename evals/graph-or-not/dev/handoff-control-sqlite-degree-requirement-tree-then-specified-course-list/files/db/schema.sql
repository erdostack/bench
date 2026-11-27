CREATE TABLE requirement (
    id         INTEGER PRIMARY KEY,
    parent_id  INTEGER REFERENCES requirement (id),   -- NULL for a programme's top-level requirement
    title      TEXT NOT NULL
);
CREATE INDEX requirement_parent ON requirement (parent_id);

-- Courses listed directly under a requirement. A course can be listed under several requirements.
CREATE TABLE requirement_course (
    requirement_id  INTEGER NOT NULL REFERENCES requirement (id),
    course_code     TEXT NOT NULL,
    PRIMARY KEY (requirement_id, course_code)
);
