CREATE TABLE product (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL,
    category   TEXT NOT NULL,
    price_eur  NUMERIC(10, 2) NOT NULL
);

-- Pairings curated by merchandising in the admin ("goes well with").
-- A pairing has no direction. Each pair is stored once, with product_a < product_b.
CREATE TABLE pairing (
    product_a   INTEGER NOT NULL REFERENCES product (id),
    product_b   INTEGER NOT NULL REFERENCES product (id),
    created_by  TEXT NOT NULL,
    created_at  TIMESTAMP NOT NULL,
    PRIMARY KEY (product_a, product_b),
    CHECK (product_a < product_b)
);
CREATE INDEX pairing_b ON pairing (product_b);
