CREATE TABLE recipe (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    yield   INTEGER NOT NULL      -- pieces per batch
);

-- One row per step of a recipe. minutes is the timed duration; NULL until someone has timed the step.
CREATE TABLE step (
    id        INTEGER PRIMARY KEY,
    recipe_id INTEGER NOT NULL REFERENCES recipe (id),
    name      TEXT NOT NULL,
    minutes   INTEGER
);

-- after_id cannot start before before_id has finished.
CREATE TABLE step_dep (
    before_id INTEGER NOT NULL REFERENCES step (id),
    after_id  INTEGER NOT NULL REFERENCES step (id),
    PRIMARY KEY (before_id, after_id)
);

CREATE TABLE daily_plan (
    day       TEXT NOT NULL,
    recipe_id INTEGER NOT NULL REFERENCES recipe (id),
    batches   INTEGER NOT NULL,
    PRIMARY KEY (day, recipe_id)
);
