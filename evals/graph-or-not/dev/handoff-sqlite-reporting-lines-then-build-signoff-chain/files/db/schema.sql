-- People directory, as exported by the HR app.
CREATE TABLE employee (
  id         INTEGER PRIMARY KEY,
  name       TEXT NOT NULL,
  grade      INTEGER NOT NULL,          -- pay grade, 1 (entry) to 9
  department TEXT
);

-- Who reports to whom. 'solid' is the line manager, 'dotted' a functional or project lead.
CREATE TABLE reporting_line (
  employee_id INTEGER NOT NULL REFERENCES employee(id),
  manager_id  INTEGER NOT NULL REFERENCES employee(id),
  kind        TEXT NOT NULL CHECK (kind IN ('solid', 'dotted')),
  PRIMARY KEY (employee_id, manager_id)
);

CREATE UNIQUE INDEX reporting_line_one_solid ON reporting_line(employee_id) WHERE kind = 'solid';
CREATE INDEX reporting_line_manager ON reporting_line(manager_id);
