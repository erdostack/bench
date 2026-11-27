-- Postgres 16, the newsroom CMS.
CREATE TABLE tag (
  id        int PRIMARY KEY,
  slug      text NOT NULL UNIQUE,
  parent_id int REFERENCES tag(id)       -- NULL for a top-level tag
);

CREATE TABLE article_tag (
  article_id bigint NOT NULL,
  tag_id     int NOT NULL REFERENCES tag(id),
  PRIMARY KEY (tag_id, article_id)
);

CREATE INDEX tag_parent ON tag (parent_id);
