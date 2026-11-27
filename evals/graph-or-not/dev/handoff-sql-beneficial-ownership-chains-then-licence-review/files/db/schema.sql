CREATE TABLE company (
    id         BIGINT PRIMARY KEY,
    reg_no     TEXT NOT NULL UNIQUE,
    name       TEXT NOT NULL,
    kind       TEXT NOT NULL,            -- 'company', 'person', 'trust', 'fund'
    dissolved  DATE
);

-- owner holds share_pct of owned. Cross-holdings exist, so chains can loop.
CREATE TABLE holding (
    owner_id   BIGINT NOT NULL REFERENCES company (id),
    owned_id   BIGINT NOT NULL REFERENCES company (id),
    share_pct  NUMERIC(6, 3) NOT NULL,
    PRIMARY KEY (owner_id, owned_id)
);
CREATE INDEX holding_owned ON holding (owned_id);
