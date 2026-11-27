-- Sewer network export (asset team, monthly). SQLite.

CREATE TABLE node (
    node_id    INTEGER PRIMARY KEY,
    asset_ref  TEXT NOT NULL,          -- MH-0412, PS-07, OF-02
    kind       TEXT NOT NULL,          -- 'manhole', 'pumping_station', 'outfall'
    catchment  TEXT                    -- 'Eastgate', 'Millbrook', ...
);

-- One row per pipe, digitised in the direction of flow: water runs from us_node to ds_node.
-- kind: 'gravity'; 'rising_main' (pumped, from a pumping station); 'overflow' (relief link between two
-- sewers; where it can run either way it is digitised twice, once in each direction).
CREATE TABLE pipe (
    pipe_id      INTEGER PRIMARY KEY,
    us_node      INTEGER NOT NULL REFERENCES node(node_id),
    ds_node      INTEGER NOT NULL REFERENCES node(node_id),
    diameter_mm  INTEGER,
    kind         TEXT NOT NULL
);

CREATE INDEX pipe_ds ON pipe(ds_node);
CREATE INDEX pipe_us ON pipe(us_node);
