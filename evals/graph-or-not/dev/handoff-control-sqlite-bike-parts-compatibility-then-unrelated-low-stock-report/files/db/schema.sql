-- The shop's SQLite database. part and compat are rebuilt weekly from the supplier catalogue.
CREATE TABLE store (
  id   INTEGER PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE part (
  id            INTEGER PRIMARY KEY,
  sku           TEXT NOT NULL UNIQUE,
  name          TEXT NOT NULL,
  reorder_level INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE stock (
  store_id INTEGER NOT NULL REFERENCES store(id),
  part_id  INTEGER NOT NULL REFERENCES part(id),
  on_hand  INTEGER NOT NULL,
  PRIMARY KEY (store_id, part_id)
);

-- part_a and part_b fit together (stored once per pair, part_a < part_b).
CREATE TABLE compat (
  part_a INTEGER NOT NULL REFERENCES part(id),
  part_b INTEGER NOT NULL REFERENCES part(id),
  note   TEXT NOT NULL DEFAULT '',
  PRIMARY KEY (part_a, part_b)
);
