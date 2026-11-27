CREATE TABLE party (
    id       BIGINT PRIMARY KEY,
    name     TEXT NOT NULL,
    country  TEXT NOT NULL,
    kind     TEXT NOT NULL CHECK (kind IN ('us', 'supplier'))
);

CREATE TABLE item (
    id       BIGINT PRIMARY KEY,
    sku      TEXT NOT NULL UNIQUE,
    name     TEXT NOT NULL,
    made_by  BIGINT NOT NULL REFERENCES party (id)
);

-- supplier delivers item to buyer. Purchasing also records what our suppliers buy from theirs when they tell us.
CREATE TABLE supplies (
    supplier_id  BIGINT NOT NULL REFERENCES party (id),
    buyer_id     BIGINT NOT NULL REFERENCES party (id),
    item_id      BIGINT NOT NULL REFERENCES item (id),
    since        DATE NOT NULL,
    PRIMARY KEY (supplier_id, buyer_id, item_id)
);
CREATE INDEX supplies_buyer ON supplies (buyer_id);
