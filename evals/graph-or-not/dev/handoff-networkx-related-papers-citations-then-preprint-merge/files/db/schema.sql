CREATE TABLE paper (
    id     BIGINT PRIMARY KEY,
    doi    TEXT UNIQUE,
    title  TEXT NOT NULL,
    year   INTEGER
);

CREATE TABLE citation (
    citing  BIGINT NOT NULL REFERENCES paper (id),
    cited   BIGINT NOT NULL REFERENCES paper (id),
    PRIMARY KEY (citing, cited)
);
CREATE INDEX citation_cited ON citation (cited);
