CREATE TABLE crib_item (
    id    INTEGER PRIMARY KEY,
    code  TEXT NOT NULL UNIQUE,
    kind  TEXT NOT NULL CHECK (kind IN ('tool', 'kit')),
    title TEXT NOT NULL
);

-- item_id is packed in kit_id, qty of them. item_id may itself be a kit.
CREATE TABLE kit_line (
    kit_id  INTEGER NOT NULL REFERENCES crib_item (id),
    item_id INTEGER NOT NULL REFERENCES crib_item (id),
    qty     INTEGER NOT NULL CHECK (qty > 0),
    PRIMARY KEY (kit_id, item_id)
);

CREATE TABLE issue (
    id        INTEGER PRIMARY KEY,
    item_id   INTEGER NOT NULL REFERENCES crib_item (id),
    badge     TEXT NOT NULL,
    issued_at TEXT NOT NULL,
    returned_at TEXT
);
