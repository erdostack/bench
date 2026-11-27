CREATE TABLE designer (id INTEGER PRIMARY KEY, name TEXT NOT NULL);
CREATE TABLE credit (game TEXT NOT NULL, designer_id INTEGER NOT NULL REFERENCES designer(id));
CREATE INDEX credit_game ON credit(game);
