CREATE TABLE tbl (
    name   TEXT PRIMARY KEY,
    layer  TEXT NOT NULL CHECK (layer IN ('raw', 'staging', 'mart')),
    owner  TEXT
);

CREATE TABLE edge (
    src  TEXT NOT NULL,
    dst  TEXT NOT NULL,
    job  TEXT NOT NULL,
    PRIMARY KEY (src, dst, job)
);

CREATE INDEX edge_dst ON edge (dst);
