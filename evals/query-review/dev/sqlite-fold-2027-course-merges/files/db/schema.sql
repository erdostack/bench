CREATE TABLE courses (
  course_id INTEGER PRIMARY KEY,
  code      TEXT NOT NULL UNIQUE,     -- e.g. 'CHEM 101', 'CHEM 101L'
  title     TEXT NOT NULL,
  dept      TEXT NOT NULL,
  credits   INTEGER NOT NULL
);

-- course_id cannot be taken before required_id has been passed with at least min_grade.
CREATE TABLE requires (
  course_id   INTEGER NOT NULL REFERENCES courses(course_id),
  required_id INTEGER NOT NULL REFERENCES courses(course_id),
  min_grade   TEXT NOT NULL CHECK (min_grade IN ('D', 'C-', 'C', 'B-', 'B')),
  PRIMARY KEY (course_id, required_id)
);
CREATE INDEX requires_required ON requires(required_id);

CREATE TABLE offerings (
  offering_id INTEGER PRIMARY KEY,
  course_id   INTEGER NOT NULL REFERENCES courses(course_id),
  term        TEXT NOT NULL,          -- '2026FA', '2027SP', ...
  section     INTEGER NOT NULL,
  seats       INTEGER NOT NULL
);
CREATE INDEX offerings_course ON offerings(course_id);
