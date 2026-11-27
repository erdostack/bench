CREATE TABLE ticket (
    id          BIGINT PRIMARY KEY,
    project_id  BIGINT NOT NULL,
    title       TEXT   NOT NULL,
    status      TEXT   NOT NULL
);

-- blocker_id blocks ticket_id.
CREATE TABLE ticket_block (
    ticket_id   BIGINT NOT NULL REFERENCES ticket (id),
    blocker_id  BIGINT NOT NULL REFERENCES ticket (id),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (ticket_id, blocker_id)
);
CREATE INDEX ticket_block_blocker ON ticket_block (blocker_id);
