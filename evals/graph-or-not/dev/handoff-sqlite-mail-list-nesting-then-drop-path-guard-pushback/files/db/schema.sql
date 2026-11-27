-- The mail relay's list config (SQLite, synced from the directory every 5 minutes).
CREATE TABLE list (
  id      INTEGER PRIMARY KEY,
  address TEXT NOT NULL UNIQUE,      -- e.g. team-payments@lists.example.org
  owner   TEXT NOT NULL
);

-- A member is either a mailbox (address) or another list (sublist_id), never both.
CREATE TABLE member (
  list_id    INTEGER NOT NULL REFERENCES list(id),
  address    TEXT,
  sublist_id INTEGER REFERENCES list(id),
  CHECK ((address IS NULL) <> (sublist_id IS NULL))
);

CREATE INDEX member_by_list ON member (list_id);
