CREATE TABLE person (
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL,
  email TEXT NOT NULL UNIQUE,
  title TEXT
);

CREATE TABLE team (
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL,
  kind  TEXT NOT NULL DEFAULT 'team' CHECK (kind IN ('team', 'project', 'location', 'company'))
);

-- One row per stint in a team. left_at is set when someone leaves; a person who rejoins gets a new row.
CREATE TABLE team_member (
  id        INTEGER PRIMARY KEY,
  team_id   INTEGER NOT NULL REFERENCES team(id),
  person_id INTEGER NOT NULL REFERENCES person(id),
  joined_at TEXT NOT NULL,
  left_at   TEXT
);

CREATE INDEX team_member_person ON team_member(person_id);
CREATE INDEX team_member_team ON team_member(team_id);
