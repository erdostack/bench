CREATE TABLE judge (
    id      INTEGER PRIMARY KEY,
    name    TEXT NOT NULL,
    school  TEXT NOT NULL          -- the school the judge teaches at or is a parent at
);

CREATE TABLE judge_category (
    judge_id  INTEGER NOT NULL REFERENCES judge (id),
    category  TEXT NOT NULL,
    PRIMARY KEY (judge_id, category)
);

CREATE TABLE project (
    id        INTEGER PRIMARY KEY,
    title     TEXT NOT NULL,
    school    TEXT NOT NULL,
    category  TEXT NOT NULL
);
