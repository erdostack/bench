CREATE TABLE valve (
    id  INTEGER PRIMARY KEY,         -- 0 is the pump
    x   REAL NOT NULL,               -- metres east of the block's corner post
    y   REAL NOT NULL                -- metres north
);

-- Trench runs the surveyor approved. Both directions are the same run.
CREATE TABLE candidate_run (
    a              INTEGER NOT NULL REFERENCES valve (id),
    b              INTEGER NOT NULL REFERENCES valve (id),
    length_m       REAL NOT NULL,
    crosses_track  INTEGER NOT NULL DEFAULT 0,    -- 1 if the run crosses the farm track
    PRIMARY KEY (a, b)
);
