-- trailmark (PostgreSQL 16)

CREATE TABLE tables (
    id         bigint PRIMARY KEY,
    full_name  text NOT NULL UNIQUE
);

CREATE TABLE columns (
    id        bigint PRIMARY KEY,
    table_id  bigint NOT NULL REFERENCES tables (id),
    name      text NOT NULL
);

-- downstream_column_id is computed from upstream_column_id by job_id.
CREATE TABLE column_edges (
    upstream_column_id    bigint NOT NULL REFERENCES columns (id),
    downstream_column_id  bigint NOT NULL REFERENCES columns (id),
    job_id                bigint NOT NULL,
    transform             text,
    last_seen             timestamptz NOT NULL,
    PRIMARY KEY (upstream_column_id, downstream_column_id, job_id)
);
CREATE INDEX column_edges_down_idx ON column_edges (downstream_column_id);

-- Derived nightly from column_edges for the catalog's overview page.
CREATE TABLE table_edges (
    upstream_table_id    bigint NOT NULL REFERENCES tables (id),
    downstream_table_id  bigint NOT NULL REFERENCES tables (id),
    PRIMARY KEY (upstream_table_id, downstream_table_id)
);
