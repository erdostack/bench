CREATE TABLE researcher (
    id     INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    orcid  TEXT
);

CREATE TABLE institution (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL
);

-- Current and past affiliations.
CREATE TABLE affiliation (
    researcher_id   INTEGER NOT NULL REFERENCES researcher (id),
    institution_id  INTEGER NOT NULL REFERENCES institution (id),
    since           TEXT NOT NULL,
    until           TEXT
);

-- Published papers from the bibliographic index. published_on is an ISO date.
CREATE TABLE paper (
    id            INTEGER PRIMARY KEY,
    title         TEXT NOT NULL,
    published_on  TEXT NOT NULL
);

CREATE TABLE authorship (
    paper_id       INTEGER NOT NULL REFERENCES paper (id),
    researcher_id  INTEGER NOT NULL REFERENCES researcher (id),
    position       INTEGER NOT NULL,
    PRIMARY KEY (paper_id, researcher_id)
);
CREATE INDEX authorship_researcher ON authorship (researcher_id);

-- Manuscripts under review.
CREATE TABLE submission (
    id            INTEGER PRIMARY KEY,
    title         TEXT NOT NULL,
    submitted_on  TEXT NOT NULL
);

CREATE TABLE submission_author (
    submission_id  INTEGER NOT NULL REFERENCES submission (id),
    researcher_id  INTEGER NOT NULL REFERENCES researcher (id),
    PRIMARY KEY (submission_id, researcher_id)
);
