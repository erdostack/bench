-- Network inventory, owned by provisioning. Read-only for noc-impact.
CREATE TABLE device (
    id          BIGINT PRIMARY KEY,
    kind        TEXT NOT NULL,          -- 'core', 'agg', 'olt', 'cpe', 'splice'
    site_id     BIGINT NOT NULL,
    customer_facing BOOLEAN NOT NULL DEFAULT false
);

-- A fibre span or patch between two devices. Spans are not directional; rings and meshes are normal.
CREATE TABLE link (
    id        BIGINT PRIMARY KEY,
    a_end     BIGINT NOT NULL REFERENCES device (id),
    b_end     BIGINT NOT NULL REFERENCES device (id),
    status    TEXT NOT NULL DEFAULT 'up',   -- 'up', 'down', 'planned'
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX link_a ON link (a_end) WHERE status = 'up';
CREATE INDEX link_b ON link (b_end) WHERE status = 'up';
