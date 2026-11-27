CREATE TABLE account (
    id          INTEGER PRIMARY KEY,
    handle      TEXT NOT NULL,
    created_on  TEXT NOT NULL,
    banned      INTEGER NOT NULL DEFAULT 0
);

-- Signals seen at sign-in or checkout. kind is 'ip', 'device' (device id) or 'card' (payment card fingerprint).
CREATE TABLE signal (
    account_id  INTEGER NOT NULL REFERENCES account (id),
    kind        TEXT NOT NULL,
    value       TEXT NOT NULL,
    PRIMARY KEY (account_id, kind, value)
);
CREATE INDEX signal_value ON signal (kind, value);
