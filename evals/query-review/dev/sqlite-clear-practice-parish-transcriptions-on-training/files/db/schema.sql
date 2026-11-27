CREATE TABLE entity (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,          -- person | record | volume
  label TEXT NOT NULL,
  year INTEGER
);
CREATE TABLE relation (
  id INTEGER PRIMARY KEY,
  kind TEXT NOT NULL,          -- appears_in (person -> record) | in_volume (record -> volume)
  from_id INTEGER NOT NULL REFERENCES entity(id),
  to_id INTEGER NOT NULL REFERENCES entity(id),
  status TEXT NOT NULL,        -- current | superseded | disputed
  volunteer TEXT,              -- who made it: volunteer code, tutor-<name>, trn-NN for trainees on the course
  created_on TEXT NOT NULL
);
CREATE INDEX relation_volunteer ON relation(volunteer);
