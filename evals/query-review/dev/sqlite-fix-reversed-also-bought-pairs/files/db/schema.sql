CREATE TABLE products (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL
);

-- unordered pair, a < b (see docs/also_bought.md)
CREATE TABLE also_bought (
    a       INTEGER NOT NULL REFERENCES products(id),
    b       INTEGER NOT NULL REFERENCES products(id),
    orders  INTEGER NOT NULL,
    PRIMARY KEY (a, b)
) WITHOUT ROWID;
CREATE INDEX also_bought_b ON also_bought (b, a);
