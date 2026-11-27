-- riskgate (PostgreSQL 15)

CREATE TABLE accounts (
    id            bigint PRIMARY KEY,
    created_at    timestamptz NOT NULL,
    status        text NOT NULL CHECK (status IN ('active', 'frozen', 'confirmed_fraud', 'closed'))
);

CREATE TABLE entities (
    id      bigint PRIMARY KEY,
    kind    text NOT NULL CHECK (kind IN ('device', 'card', 'address', 'phone')),
    digest  bytea NOT NULL,
    UNIQUE (kind, digest)
);

-- An account used an entity. Written by the event consumer as activity happens.
CREATE TABLE links (
    account_id  bigint NOT NULL REFERENCES accounts (id),
    entity_id   bigint NOT NULL REFERENCES entities (id),
    first_seen  timestamptz NOT NULL,
    last_seen   timestamptz NOT NULL,
    PRIMARY KEY (account_id, entity_id)
);
CREATE INDEX links_entity_account_idx ON links (entity_id, account_id);

-- Maintained by the event consumer; used to skip very widely shared entities.
CREATE TABLE entity_degree (
    entity_id  bigint PRIMARY KEY REFERENCES entities (id),
    accounts   integer NOT NULL
);
