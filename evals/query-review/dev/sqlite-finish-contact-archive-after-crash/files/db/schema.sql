CREATE TABLE users (
    id      INTEGER PRIMARY KEY,
    handle  TEXT NOT NULL UNIQUE
);

CREATE TABLE contacts (
    owner_id        INTEGER NOT NULL REFERENCES users(id),
    contact_id      INTEGER NOT NULL REFERENCES users(id),
    created_at      TEXT NOT NULL,
    last_contact_at TEXT NOT NULL,
    PRIMARY KEY (owner_id, contact_id)
);
CREATE INDEX contacts_last ON contacts(last_contact_at);

CREATE TABLE contacts_archive (
    owner_id        INTEGER NOT NULL,
    contact_id      INTEGER NOT NULL,
    created_at      TEXT NOT NULL,
    last_contact_at TEXT NOT NULL,
    archived_at     TEXT NOT NULL
);
CREATE INDEX contacts_archive_owner ON contacts_archive(owner_id);
