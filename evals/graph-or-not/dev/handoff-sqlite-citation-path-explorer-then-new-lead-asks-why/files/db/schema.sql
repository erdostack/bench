CREATE TABLE paper (
    id         INTEGER PRIMARY KEY,
    doi        TEXT UNIQUE,
    year       INTEGER,
    venue_id   INTEGER,
    retracted  INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE citation (
    citing_id  INTEGER NOT NULL,
    cited_id   INTEGER NOT NULL,
    PRIMARY KEY (citing_id, cited_id)
) WITHOUT ROWID;
CREATE INDEX citation_cited ON citation (cited_id, citing_id);
