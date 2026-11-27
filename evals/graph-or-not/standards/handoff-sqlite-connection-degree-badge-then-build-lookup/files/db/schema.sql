-- circle: members and friendships. SQLite.

CREATE TABLE person (
    id             INTEGER PRIMARY KEY,
    first_name     TEXT NOT NULL,
    last_name      TEXT NOT NULL,
    gender         TEXT,
    birthday       TEXT,
    creation_date  TEXT NOT NULL,
    location_ip    TEXT,
    browser_used   TEXT,
    city_id        INTEGER
);

-- One row per friendship. requester_id is the member who sent the friend request and accepter_id the one who
-- accepted it; the pair is never stored a second time the other way round.
CREATE TABLE knows (
    requester_id   INTEGER NOT NULL REFERENCES person(id),
    accepter_id    INTEGER NOT NULL REFERENCES person(id),
    creation_date  TEXT NOT NULL,
    PRIMARY KEY (requester_id, accepter_id)
);

CREATE INDEX knows_accepter ON knows(accepter_id);
