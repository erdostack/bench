CREATE TABLE lot (
    id         INTEGER PRIMARY KEY,
    plant      TEXT NOT NULL,
    material   TEXT NOT NULL,
    kind       TEXT NOT NULL CHECK (kind IN ('raw', 'component', 'assembly', 'shipped')),
    made_at    TEXT NOT NULL
);

-- child_lot was made using parent_lot (qty of the parent consumed).
CREATE TABLE lot_link (
    parent_lot INTEGER NOT NULL REFERENCES lot (id),
    child_lot  INTEGER NOT NULL REFERENCES lot (id),
    qty        REAL NOT NULL,
    linked_at  TEXT NOT NULL,
    PRIMARY KEY (parent_lot, child_lot)
);
CREATE INDEX lot_link_child ON lot_link (child_lot, parent_lot);
