CREATE TABLE unit (
  id        INTEGER PRIMARY KEY,
  name      TEXT NOT NULL,
  parent_id INTEGER REFERENCES unit(id),       -- NULL for the top of the organisation
  opened_on TEXT NOT NULL,
  closed_on TEXT                                -- NULL while the unit exists
);
CREATE INDEX unit_parent ON unit(parent_id);

CREATE TABLE person (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

-- Who works in which unit, and from when to when (end_date inclusive, NULL while ongoing).
CREATE TABLE assignment (
  id         INTEGER PRIMARY KEY,
  person_id  INTEGER NOT NULL REFERENCES person(id),
  unit_id    INTEGER NOT NULL REFERENCES unit(id),
  start_date TEXT NOT NULL,
  end_date   TEXT
);
CREATE INDEX assignment_unit ON assignment(unit_id, start_date);
