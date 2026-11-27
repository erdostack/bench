DROP TABLE IF EXISTS leg;
DROP TABLE IF EXISTS waypoint;

CREATE TABLE waypoint (
  code TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  kind TEXT NOT NULL
);

CREATE TABLE leg (
  from_code TEXT NOT NULL REFERENCES waypoint(code),
  to_code   TEXT NOT NULL REFERENCES waypoint(code),
  km        NUMERIC(5, 1) NOT NULL,
  PRIMARY KEY (from_code, to_code)
);

CREATE INDEX leg_to ON leg (to_code);
