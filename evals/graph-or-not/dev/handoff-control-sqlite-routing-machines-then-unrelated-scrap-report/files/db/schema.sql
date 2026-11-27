CREATE TABLE product (id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, title TEXT NOT NULL);
CREATE TABLE machine (id INTEGER PRIMARY KEY, code TEXT NOT NULL UNIQUE, cell TEXT NOT NULL);

CREATE TABLE routing_op (
    product_id INTEGER NOT NULL REFERENCES product (id),
    seq        INTEGER NOT NULL,
    machine_id INTEGER NOT NULL REFERENCES machine (id),
    minutes    REAL NOT NULL,
    PRIMARY KEY (product_id, seq)
);

CREATE TABLE prod_log (
    id         INTEGER PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES machine (id),
    product_id INTEGER NOT NULL REFERENCES product (id),
    logged_at  TEXT NOT NULL,           -- 'YYYY-MM-DD HH:MM', local time
    produced   INTEGER NOT NULL,
    scrapped   INTEGER NOT NULL,
    status     TEXT NOT NULL CHECK (status IN ('ok', 'void'))
);
