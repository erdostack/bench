-- Item master and bills of materials, copied nightly from PLM.
CREATE TABLE item (
    id          INTEGER PRIMARY KEY,
    part_no     TEXT NOT NULL UNIQUE,
    description TEXT NOT NULL,
    uom         TEXT NOT NULL DEFAULT 'ea',
    make_buy    TEXT NOT NULL CHECK (make_buy IN ('M', 'B'))
);

-- One line per component of a made item: qty_per units of component_id go into one unit of parent_id.
CREATE TABLE bom_line (
    parent_id    INTEGER NOT NULL REFERENCES item (id),
    component_id INTEGER NOT NULL REFERENCES item (id),
    qty_per      REAL NOT NULL CHECK (qty_per > 0),
    PRIMARY KEY (parent_id, component_id)
);
CREATE INDEX bom_line_component ON bom_line (component_id);

CREATE TABLE works_order (
    id       INTEGER PRIMARY KEY,
    item_id  INTEGER NOT NULL REFERENCES item (id),
    qty      INTEGER NOT NULL,
    due      TEXT NOT NULL
);
