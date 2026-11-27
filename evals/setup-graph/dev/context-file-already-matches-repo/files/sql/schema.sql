CREATE TABLE course (
  code    TEXT PRIMARY KEY,
  title   TEXT NOT NULL,
  credits SMALLINT NOT NULL CHECK (credits > 0)
);

-- one row per edge: "needs" must be passed before "course" can be taken
CREATE TABLE prerequisite (
  course TEXT NOT NULL REFERENCES course(code),
  needs  TEXT NOT NULL REFERENCES course(code),
  PRIMARY KEY (course, needs),
  CHECK (course <> needs)
);

CREATE INDEX prerequisite_needs ON prerequisite(needs);
