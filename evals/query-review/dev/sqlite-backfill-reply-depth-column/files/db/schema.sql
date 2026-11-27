CREATE TABLE threads (
    id          INTEGER PRIMARY KEY,
    board       TEXT NOT NULL,
    title       TEXT NOT NULL,
    locked      INTEGER NOT NULL DEFAULT 0,
    last_post_at TEXT NOT NULL
);

CREATE TABLE posts (
    id          INTEGER PRIMARY KEY,
    thread_id   INTEGER NOT NULL REFERENCES threads(id),
    parent_id   INTEGER REFERENCES posts(id),
    author      TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    hidden      INTEGER NOT NULL DEFAULT 0
);
CREATE INDEX posts_parent ON posts(parent_id);
CREATE INDEX posts_thread ON posts(thread_id);
