CREATE TABLE item (
    id        INTEGER PRIMARY KEY,
    part_no   TEXT NOT NULL UNIQUE,
    title     TEXT NOT NULL,
    plant     TEXT NOT NULL
);

CREATE TABLE bom_line (
    parent_id    INTEGER NOT NULL REFERENCES item (id),
    component_id INTEGER NOT NULL REFERENCES item (id),
    qty_per      REAL NOT NULL,
    PRIMARY KEY (parent_id, component_id)
);
CREATE INDEX bom_line_component ON bom_line (component_id);

CREATE TABLE eco (
    id        INTEGER PRIMARY KEY,
    item_id   INTEGER NOT NULL REFERENCES item (id),
    opened_at TEXT NOT NULL,
    status    TEXT NOT NULL
);
