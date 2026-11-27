CREATE TABLE member (
    id          BIGINT PRIMARY KEY,
    name        TEXT NOT NULL,
    grad_year   INT  NOT NULL,
    programme   TEXT NOT NULL
);

-- A connection is stored once per direction: (a, b) and (b, a).
CREATE TABLE connection (
    member_id   BIGINT NOT NULL REFERENCES member (id),
    other_id    BIGINT NOT NULL REFERENCES member (id),
    since       DATE   NOT NULL,
    PRIMARY KEY (member_id, other_id)
);
