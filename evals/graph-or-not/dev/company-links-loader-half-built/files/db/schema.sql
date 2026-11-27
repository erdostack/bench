-- registerlens (PostgreSQL 16)

CREATE TABLE entities (
    id      bigint PRIMARY KEY,
    kind    text NOT NULL CHECK (kind IN ('company', 'person')),
    name    text NOT NULL,
    status  text
);

-- from_id is connected to to_id: officer_of, owns_share_in, registered_agent_for.
CREATE TABLE links (
    from_id     bigint NOT NULL REFERENCES entities (id),
    to_id       bigint NOT NULL REFERENCES entities (id),
    kind        text   NOT NULL,
    since       date,
    until       date,
    PRIMARY KEY (from_id, to_id, kind)
);
CREATE INDEX links_to_idx ON links (to_id, kind);
