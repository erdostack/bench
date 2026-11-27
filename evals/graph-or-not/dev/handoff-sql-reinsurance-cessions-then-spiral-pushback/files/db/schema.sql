-- Postgres 15, the treaty administration database.
CREATE TABLE party (
  id   int PRIMARY KEY,
  name text NOT NULL,
  kind text NOT NULL CHECK (kind IN ('cedant', 'reinsurer'))
);

CREATE TABLE contract (
  id          int PRIMARY KEY,
  cedant_id   int NOT NULL REFERENCES party(id),
  limit_eur   numeric(16, 2) NOT NULL,
  inception   date NOT NULL,
  expiry      date NOT NULL
);

-- `ceded_by` passes `share` of what it holds on `contract_id` to `ceded_to`.
CREATE TABLE cession (
  contract_id int NOT NULL REFERENCES contract(id),
  ceded_by    int NOT NULL REFERENCES party(id),
  ceded_to    int NOT NULL REFERENCES party(id),
  share       numeric(7, 6) NOT NULL CHECK (share > 0 AND share <= 1),
  PRIMARY KEY (contract_id, ceded_by, ceded_to)
);

CREATE INDEX cession_by ON cession (contract_id, ceded_by);
