CREATE TABLE billing_account (
  id        INTEGER PRIMARY KEY,
  iban_last TEXT,
  currency  TEXT NOT NULL DEFAULT 'EUR'
);

CREATE TABLE org (
  id                 INTEGER PRIMARY KEY,
  name               TEXT NOT NULL,
  parent_id          INTEGER REFERENCES org(id),              -- NULL for a top-level organisation
  billing_account_id INTEGER REFERENCES billing_account(id)   -- NULL when the org has no account of its own
);
CREATE INDEX org_parent ON org(parent_id);

CREATE TABLE usage_line (
  id       INTEGER PRIMARY KEY,
  org_id   INTEGER NOT NULL REFERENCES org(id),
  month    TEXT NOT NULL,
  amount   REAL NOT NULL
);
