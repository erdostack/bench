-- netmodel (PostgreSQL). Network model for the distribution grid.

CREATE TABLE node (
    node_id      bigint PRIMARY KEY,
    kind         text NOT NULL,          -- 'busbar', 'joint', 'switch', 'transformer', 'service_point'
    region       text NOT NULL,
    customers    integer NOT NULL DEFAULT 0
);

CREATE TABLE segment (
    segment_id   bigint PRIMARY KEY,
    a_node       bigint NOT NULL REFERENCES node(node_id),
    b_node       bigint NOT NULL REFERENCES node(node_id),
    conductor    text,
    is_closed    boolean NOT NULL DEFAULT true   -- switching state; false for an open point
);

CREATE INDEX segment_a ON segment (a_node) WHERE is_closed;
CREATE INDEX segment_b ON segment (b_node) WHERE is_closed;
