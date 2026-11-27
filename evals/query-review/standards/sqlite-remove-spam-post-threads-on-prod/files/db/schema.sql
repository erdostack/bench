CREATE TABLE person (
    id            INTEGER PRIMARY KEY,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    gender        TEXT,
    birthday      TEXT,
    creation_date TEXT NOT NULL,
    location_ip   TEXT,
    browser_used  TEXT
);
CREATE TABLE knows (
    person1_id    INTEGER NOT NULL,
    person2_id    INTEGER NOT NULL,
    creation_date TEXT NOT NULL
);
CREATE TABLE forum (
    id            INTEGER PRIMARY KEY,
    title         TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    moderator_id  INTEGER
);
CREATE TABLE forum_member (
    forum_id      INTEGER NOT NULL,
    person_id     INTEGER NOT NULL,
    join_date     TEXT NOT NULL
);
CREATE TABLE tag (
    id            INTEGER PRIMARY KEY,
    name          TEXT NOT NULL UNIQUE
);
CREATE TABLE post (
    id            INTEGER PRIMARY KEY,
    forum_id      INTEGER NOT NULL,
    creator_id    INTEGER NOT NULL,
    creation_date TEXT NOT NULL,
    location_ip   TEXT,
    browser_used  TEXT,
    language      TEXT,
    length        INTEGER NOT NULL,
    content       TEXT
);
CREATE TABLE comment (
    id               INTEGER PRIMARY KEY,
    creator_id       INTEGER NOT NULL,
    creation_date    TEXT NOT NULL,
    location_ip      TEXT,
    browser_used     TEXT,
    length           INTEGER NOT NULL,
    content          TEXT,
    reply_of_post    INTEGER,
    reply_of_comment INTEGER
);
CREATE TABLE likes (
    person_id     INTEGER NOT NULL,
    message_id    INTEGER NOT NULL,
    creation_date TEXT NOT NULL
);
CREATE TABLE message_tag (
    message_id    INTEGER NOT NULL,
    tag_id        INTEGER NOT NULL
);
CREATE INDEX knows_p1 ON knows (person1_id);
CREATE INDEX knows_p2 ON knows (person2_id);
CREATE INDEX member_person ON forum_member (person_id);
CREATE INDEX post_forum ON post (forum_id);
CREATE INDEX post_creator ON post (creator_id);
CREATE INDEX comment_reply_post ON comment (reply_of_post);
CREATE INDEX comment_reply_comment ON comment (reply_of_comment);
CREATE INDEX comment_creator ON comment (creator_id);
CREATE INDEX likes_message ON likes (message_id);
CREATE INDEX likes_person ON likes (person_id);
CREATE INDEX message_tag_message ON message_tag (message_id);
