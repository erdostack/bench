CREATE TABLE recipes (
    id        INTEGER PRIMARY KEY,
    slug      TEXT NOT NULL UNIQUE,
    source    TEXT NOT NULL,          -- 'editorial', 'community' or '2019-import'
    servings  INTEGER NOT NULL
);
CREATE TABLE ingredients (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);
CREATE TABLE uses (
    recipe_id      INTEGER NOT NULL REFERENCES recipes(id),
    ingredient_id  INTEGER NOT NULL REFERENCES ingredients(id),
    qty            REAL NOT NULL,
    unit           TEXT NOT NULL,
    PRIMARY KEY (recipe_id, ingredient_id)
);
CREATE INDEX uses_ingredient ON uses (ingredient_id);
CREATE TABLE job_progress (
    job      TEXT PRIMARY KEY,
    last_id  INTEGER NOT NULL
);
