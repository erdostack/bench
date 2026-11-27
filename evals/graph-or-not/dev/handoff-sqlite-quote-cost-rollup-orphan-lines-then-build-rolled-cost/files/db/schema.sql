CREATE TABLE item (
    id          INTEGER PRIMARY KEY,
    part_no     TEXT NOT NULL UNIQUE,
    kind        TEXT NOT NULL CHECK (kind IN ('made', 'bought')),
    std_cost    REAL,              -- bought items
    labour_cost REAL               -- made items: labour and machine time per unit
);

CREATE TABLE bom_line (
    parent_id    INTEGER NOT NULL REFERENCES item (id),
    component_id INTEGER NOT NULL REFERENCES item (id),
    qty          REAL NOT NULL,
    PRIMARY KEY (parent_id, component_id)
);
