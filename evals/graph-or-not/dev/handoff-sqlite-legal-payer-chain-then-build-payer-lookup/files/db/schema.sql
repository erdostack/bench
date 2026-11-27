CREATE TABLE account (
    id                 INTEGER PRIMARY KEY,
    name               TEXT NOT NULL,
    status             TEXT NOT NULL DEFAULT 'active',   -- active, suspended, closed
    parent_account_id  INTEGER REFERENCES account (id),  -- parent company, from the CRM import
    created_at         TIMESTAMP NOT NULL
);

-- Relationships between accounts, maintained by account management.
--   kind = 'legal'    the child is a subsidiary of the parent
--   kind = 'finance'  the parent holds the budget the child's spend is allocated to
--   kind = 'sales'    the same account team covers both
CREATE TABLE account_link (
    child_id   INTEGER NOT NULL REFERENCES account (id),
    parent_id  INTEGER NOT NULL REFERENCES account (id),
    kind       TEXT NOT NULL CHECK (kind IN ('legal', 'finance', 'sales')),
    since      DATE NOT NULL,
    PRIMARY KEY (child_id, kind)
);
CREATE INDEX account_link_parent ON account_link (parent_id, kind);

CREATE TABLE usage_line (
    id          INTEGER PRIMARY KEY,
    account_id  INTEGER NOT NULL REFERENCES account (id),
    period      TEXT NOT NULL,     -- '2026-11'
    amount_eur  NUMERIC(12, 2) NOT NULL
);
