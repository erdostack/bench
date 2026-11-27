CREATE TABLE org (
  id        INTEGER PRIMARY KEY,
  name      TEXT NOT NULL,
  country   TEXT,
  parent_id INTEGER REFERENCES org(id)          -- NULL for a group's top organisation
);
CREATE INDEX org_parent ON org(parent_id);

CREATE TABLE invoice (
  id         INTEGER PRIMARY KEY,
  org_id     INTEGER NOT NULL REFERENCES org(id),
  issued_on  TEXT NOT NULL,
  amount_eur REAL NOT NULL
);
CREATE INDEX invoice_org ON invoice(org_id, issued_on);

CREATE TABLE org_rollup (
  org_id      INTEGER PRIMARY KEY REFERENCES org(id),
  as_of       TEXT NOT NULL,
  revenue_12m REAL NOT NULL
);
