-- District heating network model. SQLite.

CREATE TABLE node (
    node_id    INTEGER PRIMARY KEY,
    kind       TEXT NOT NULL,        -- 'plant', 'junction', 'substation'
    building   TEXT                  -- building served, for substations
);

-- Pipes carry flow and return as a pair; one row per pipe pair. Ring mains mean there are loops.
CREATE TABLE pipe (
    pipe_id   INTEGER PRIMARY KEY,
    a_node    INTEGER NOT NULL REFERENCES node(node_id),
    b_node    INTEGER NOT NULL REFERENCES node(node_id),
    dn        INTEGER                -- nominal diameter, mm
);

CREATE INDEX pipe_a ON pipe(a_node);
CREATE INDEX pipe_b ON pipe(b_node);
