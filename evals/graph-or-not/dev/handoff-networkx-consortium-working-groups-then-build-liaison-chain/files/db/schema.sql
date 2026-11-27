CREATE TABLE organisation (
  id      INTEGER PRIMARY KEY,
  name    TEXT NOT NULL,
  country TEXT
);

CREATE TABLE working_group (
  code TEXT PRIMARY KEY,            -- e.g. 'WG-017'
  name TEXT NOT NULL
);

CREATE TABLE membership (
  org_id            INTEGER NOT NULL REFERENCES organisation(id),
  group_code        TEXT NOT NULL REFERENCES working_group(code),
  role              TEXT NOT NULL CHECK (role IN ('chair', 'member', 'observer')),
  meetings_per_year INTEGER NOT NULL DEFAULT 0,       -- meetings the org attended in the last 12 months
  PRIMARY KEY (org_id, group_code)
);
CREATE INDEX membership_group ON membership(group_code);
