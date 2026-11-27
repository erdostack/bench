-- Pager configuration. The admin UI exports it as a SQLite file and every pager node gets a copy.
CREATE TABLE team (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE person (
  id    INTEGER PRIMARY KEY,
  name  TEXT NOT NULL,
  phone TEXT
);

CREATE TABLE escalation_policy (
  id            INTEGER PRIMARY KEY,
  team_id       INTEGER NOT NULL REFERENCES team(id),
  name          TEXT NOT NULL,
  ack_timeout_s INTEGER NOT NULL DEFAULT 300,                 -- wait this long for an ack before escalating
  escalates_to  INTEGER REFERENCES escalation_policy(id)       -- next policy if nobody acks; NULL = nobody further
);

CREATE TABLE policy_target (
  policy_id INTEGER NOT NULL REFERENCES escalation_policy(id),
  person_id INTEGER NOT NULL REFERENCES person(id),
  PRIMARY KEY (policy_id, person_id)
);

CREATE INDEX escalation_policy_team ON escalation_policy(team_id);
