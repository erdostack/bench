CREATE TABLE accounts (
    id       INTEGER PRIMARY KEY,
    holder   TEXT NOT NULL,
    kind     TEXT NOT NULL CHECK (kind IN ('personal', 'business', 'exchange')),
    opened   TEXT NOT NULL
);

CREATE TABLE transfers (
    id            INTEGER PRIMARY KEY,
    src           INTEGER NOT NULL REFERENCES accounts(id),
    dst           INTEGER NOT NULL REFERENCES accounts(id),
    amount_cents  INTEGER NOT NULL,
    sent_at       TEXT NOT NULL
);

CREATE INDEX transfers_src ON transfers(src);
CREATE INDEX transfers_dst ON transfers(dst);
CREATE INDEX transfers_sent_at ON transfers(sent_at);
