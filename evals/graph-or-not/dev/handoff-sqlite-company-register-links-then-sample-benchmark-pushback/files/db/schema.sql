-- Organisations and people from the public registers, and every link between them.
CREATE TABLE entity (
  id      INTEGER PRIMARY KEY,
  kind    TEXT NOT NULL CHECK (kind IN ('company', 'person', 'public_body', 'address')),
  name    TEXT NOT NULL,
  reg_no  TEXT                                 -- register number for companies and public bodies
);

-- kind: director_of, secretary_of, shareholder_of, owns, registered_at, lives_at, awarded_to, official_of,
--       partner_of, successor_of, branch_of
CREATE TABLE relation (
  src     INTEGER NOT NULL REFERENCES entity(id),
  dst     INTEGER NOT NULL REFERENCES entity(id),
  kind    TEXT NOT NULL,
  since   TEXT,
  until   TEXT
);
CREATE INDEX relation_src ON relation(src, kind);
CREATE INDEX relation_dst ON relation(dst, kind);
