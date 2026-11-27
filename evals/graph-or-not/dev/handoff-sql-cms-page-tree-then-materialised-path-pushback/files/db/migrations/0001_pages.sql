CREATE TABLE page (
    id         BIGINT PRIMARY KEY,
    site_id    INT NOT NULL,
    parent_id  BIGINT REFERENCES page (id),
    slug       TEXT NOT NULL,
    title      TEXT NOT NULL,
    published  BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE (parent_id, slug)
);
CREATE INDEX page_parent ON page (parent_id);
