CREATE TABLE articles (
    id        INTEGER PRIMARY KEY,
    slug      TEXT NOT NULL UNIQUE,
    title     TEXT NOT NULL,
    locale    TEXT NOT NULL DEFAULT 'en'
);

-- "Related articles" edges, shown under src in score order (pinned first).
-- origin 'auto': written by the similarity model (score = cosine similarity);
-- origin 'editor': added by hand in the CMS (score NULL).
CREATE TABLE related (
    id      INTEGER PRIMARY KEY,
    src     INTEGER NOT NULL REFERENCES articles(id),
    dst     INTEGER NOT NULL REFERENCES articles(id),
    origin  TEXT NOT NULL CHECK (origin IN ('auto', 'editor')),
    score   REAL,
    pinned  INTEGER NOT NULL DEFAULT 0,
    UNIQUE (src, dst)
);
CREATE INDEX related_dst ON related (dst);

-- 0012
CREATE TRIGGER related_keep_pins BEFORE DELETE ON related
WHEN old.pinned = 1
BEGIN
    SELECT RAISE(IGNORE);
END;
