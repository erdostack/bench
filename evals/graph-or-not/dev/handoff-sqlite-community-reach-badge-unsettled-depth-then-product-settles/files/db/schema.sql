CREATE TABLE member (
    id          INTEGER PRIMARY KEY,
    handle      TEXT NOT NULL UNIQUE,
    joined_on   TEXT NOT NULL
);

-- follower_id follows followed_id.
CREATE TABLE follow (
    follower_id  INTEGER NOT NULL REFERENCES member (id),
    followed_id  INTEGER NOT NULL REFERENCES member (id),
    since        TEXT NOT NULL,
    PRIMARY KEY (follower_id, followed_id)
) WITHOUT ROWID;
CREATE INDEX follow_followed ON follow (followed_id, follower_id);
