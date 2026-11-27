CREATE TABLE folder (
    id         BIGINT PRIMARY KEY,
    parent_id  BIGINT REFERENCES folder (id),      -- NULL for a root folder
    owner_id   BIGINT NOT NULL,
    name       TEXT NOT NULL,
    moved_at   TIMESTAMPTZ
);
CREATE INDEX folder_parent_idx ON folder (parent_id);

CREATE TABLE share (
    folder_id   BIGINT NOT NULL REFERENCES folder (id),
    grantee_id  BIGINT NOT NULL,
    role        TEXT NOT NULL CHECK (role IN ('viewer', 'editor')),
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (folder_id, grantee_id)
);
