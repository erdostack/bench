-- Finance app ledger (SQLite).
CREATE TABLE account (
  id        INTEGER PRIMARY KEY,
  parent_id INTEGER REFERENCES account(id),     -- NULL for the top of a branch (Assets, Liabilities, ...)
  code      TEXT NOT NULL UNIQUE,
  name      TEXT NOT NULL
);

-- The chart of accounts is a tree. These triggers reject any insert or parent change that would put an account
-- below itself, so walking parent_id always ends at a top-level account.
CREATE TRIGGER account_no_loop_insert BEFORE INSERT ON account
WHEN NEW.parent_id IS NOT NULL AND (NEW.parent_id = NEW.id OR EXISTS (
  WITH RECURSIVE up(id) AS (
    SELECT NEW.parent_id
    UNION
    SELECT a.parent_id FROM account a JOIN up ON a.id = up.id WHERE a.parent_id IS NOT NULL
  )
  SELECT 1 FROM up WHERE id = NEW.id))
BEGIN
  SELECT RAISE(ABORT, 'account hierarchy would contain a loop');
END;

CREATE TRIGGER account_no_loop_update BEFORE UPDATE OF parent_id ON account
WHEN NEW.parent_id IS NOT NULL AND (NEW.parent_id = NEW.id OR EXISTS (
  WITH RECURSIVE up(id) AS (
    SELECT NEW.parent_id
    UNION
    SELECT a.parent_id FROM account a JOIN up ON a.id = up.id WHERE a.parent_id IS NOT NULL
  )
  SELECT 1 FROM up WHERE id = NEW.id))
BEGIN
  SELECT RAISE(ABORT, 'account hierarchy would contain a loop');
END;

CREATE TABLE posting (
  id           INTEGER PRIMARY KEY,
  account_id   INTEGER NOT NULL REFERENCES account(id),
  posted_on    TEXT NOT NULL,          -- 'YYYY-MM-DD'
  amount_cents INTEGER NOT NULL        -- debit positive, credit negative
);

CREATE INDEX account_parent ON account (parent_id);
CREATE INDEX posting_by_account ON posting (account_id, posted_on);
