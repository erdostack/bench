CREATE TABLE category (
    id         BIGINT PRIMARY KEY,
    parent_id  BIGINT REFERENCES category (id),
    slug       TEXT NOT NULL UNIQUE,
    name       TEXT NOT NULL
);
CREATE INDEX category_parent ON category (parent_id);

CREATE TABLE product (
    id           BIGINT PRIMARY KEY,
    category_id  BIGINT NOT NULL REFERENCES category (id),
    title        TEXT NOT NULL,
    price_cents  INTEGER NOT NULL,
    rank         REAL NOT NULL DEFAULT 0,
    listed       BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX product_category_rank ON product (category_id, rank DESC) WHERE listed;
