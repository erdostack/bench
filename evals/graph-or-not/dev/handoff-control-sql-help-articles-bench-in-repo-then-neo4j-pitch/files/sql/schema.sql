CREATE TABLE article (
    id         BIGINT PRIMARY KEY,
    slug       TEXT NOT NULL UNIQUE,
    title      TEXT NOT NULL,
    product    TEXT NOT NULL,
    published  BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE article_link (
    article_id  BIGINT NOT NULL REFERENCES article (id),
    target_id   BIGINT NOT NULL REFERENCES article (id),
    position    INT    NOT NULL,
    PRIMARY KEY (article_id, target_id)
);
