CREATE TABLE groups (
    id         INTEGER PRIMARY KEY,
    name       TEXT NOT NULL UNIQUE,
    updated_at TEXT NOT NULL
);

-- child_id is nested in parent_id: members of the child are members of the parent.
CREATE TABLE group_edges (
    parent_id INTEGER NOT NULL REFERENCES groups(id),
    child_id  INTEGER NOT NULL REFERENCES groups(id),
    added_at  TEXT NOT NULL,
    PRIMARY KEY (parent_id, child_id),
    CHECK (parent_id <> child_id)
) WITHOUT ROWID;

CREATE INDEX group_edges_child ON group_edges(child_id);

-- Derived: descendant_id is nested in ancestor_id, directly or through other groups.
CREATE TABLE reach (
    ancestor_id   INTEGER NOT NULL,
    descendant_id INTEGER NOT NULL,
    PRIMARY KEY (ancestor_id, descendant_id)
) WITHOUT ROWID;

CREATE TABLE job_state (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
