CREATE TABLE person (
    id            INTEGER PRIMARY KEY,
    first_name    TEXT NOT NULL,
    last_name     TEXT NOT NULL,
    creation_date TEXT NOT NULL,
    browser_used  TEXT
);
CREATE TABLE knows (
    person1_id    INTEGER NOT NULL,
    person2_id    INTEGER NOT NULL,
    creation_date TEXT NOT NULL
);
CREATE TABLE forum (
    id            INTEGER PRIMARY KEY,
    title         TEXT NOT NULL UNIQUE,
    creation_date TEXT NOT NULL,
    moderator_id  INTEGER
);
CREATE TABLE has_member (
    forum_id      INTEGER NOT NULL,
    person_id     INTEGER NOT NULL,
    join_date     TEXT NOT NULL,
    PRIMARY KEY (forum_id, person_id)
);
CREATE TABLE post (
    id            INTEGER PRIMARY KEY,
    forum_id      INTEGER NOT NULL,
    creator_id    INTEGER NOT NULL,
    creation_date TEXT NOT NULL,
    content       TEXT
);
CREATE TABLE comment (
    id            INTEGER PRIMARY KEY,
    creator_id    INTEGER NOT NULL,
    reply_of      INTEGER NOT NULL,
    creation_date TEXT NOT NULL,
    content       TEXT
);
CREATE TABLE likes (
    person_id     INTEGER NOT NULL,
    message_id    INTEGER NOT NULL,
    creation_date TEXT NOT NULL
);
CREATE INDEX member_person ON has_member (person_id);
