CREATE TABLE principal (
    id    BIGINT PRIMARY KEY,
    kind  TEXT NOT NULL CHECK (kind IN ('user', 'group')),
    name  TEXT NOT NULL
);

-- member_id is in group_id. A member can be a user or another group.
CREATE TABLE membership (
    member_id  BIGINT NOT NULL REFERENCES principal (id),
    group_id   BIGINT NOT NULL REFERENCES principal (id),
    PRIMARY KEY (member_id, group_id)
);
CREATE INDEX membership_group_idx ON membership (group_id);

CREATE TABLE grant_ (
    principal_id  BIGINT NOT NULL REFERENCES principal (id),
    resource_id   BIGINT NOT NULL,
    role          TEXT NOT NULL CHECK (role IN ('read', 'write', 'admin')),
    PRIMARY KEY (principal_id, resource_id, role)
);
