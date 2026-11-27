CREATE TABLE member (
    id           INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    joined_on    DATE NOT NULL,
    referred_by  INTEGER REFERENCES member (id),   -- who brought this member in, if anyone
    status       TEXT NOT NULL DEFAULT 'active'     -- active, frozen, cancelled
);
CREATE INDEX member_referred_by ON member (referred_by);

CREATE TABLE bonus (
    id         INTEGER PRIMARY KEY,
    member_id  INTEGER NOT NULL REFERENCES member (id),
    source_id  INTEGER NOT NULL REFERENCES member (id),
    level      INTEGER NOT NULL,
    month      TEXT NOT NULL
);
