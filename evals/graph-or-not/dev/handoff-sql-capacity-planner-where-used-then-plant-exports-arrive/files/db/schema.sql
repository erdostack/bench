CREATE TABLE item (
    id        INTEGER PRIMARY KEY,
    plant     TEXT NOT NULL,
    part_no   TEXT NOT NULL,
    make_buy  TEXT NOT NULL
);

CREATE TABLE bom_line (
    parent_id    INTEGER NOT NULL REFERENCES item (id),
    component_id INTEGER NOT NULL REFERENCES item (id),
    qty_per      REAL NOT NULL,
    PRIMARY KEY (parent_id, component_id)
);
CREATE INDEX bom_line_component ON bom_line (component_id);

CREATE TABLE component_change (
    run_id       INTEGER NOT NULL,
    component_id INTEGER NOT NULL REFERENCES item (id),
    PRIMARY KEY (run_id, component_id)
);
