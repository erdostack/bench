CREATE TABLE paper (
    id     INTEGER PRIMARY KEY,
    title  TEXT NOT NULL,
    year   INTEGER NOT NULL
);

-- One row per reference: citing_id lists cited_id in its bibliography.
CREATE TABLE cites (
    citing_id  INTEGER NOT NULL REFERENCES paper (id),
    cited_id   INTEGER NOT NULL REFERENCES paper (id),
    PRIMARY KEY (citing_id, cited_id)
);
