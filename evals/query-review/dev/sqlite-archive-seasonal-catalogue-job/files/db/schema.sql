CREATE TABLE categories (
    id        INTEGER PRIMARY KEY,
    parent_id INTEGER REFERENCES categories(id),
    name      TEXT NOT NULL,
    archived  INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX categories_parent ON categories(parent_id);

CREATE TABLE products (
    id          INTEGER PRIMARY KEY,
    sku         TEXT NOT NULL UNIQUE,
    category_id INTEGER NOT NULL REFERENCES categories(id),
    title       TEXT NOT NULL,
    archived    INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX products_category ON products(category_id);
