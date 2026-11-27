CREATE TABLE users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE);
CREATE TABLE groups (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE);
CREATE TABLE resources (id INTEGER PRIMARY KEY, path TEXT NOT NULL UNIQUE);

CREATE TABLE user_groups (
    user_id  INTEGER NOT NULL REFERENCES users(id),
    group_id INTEGER NOT NULL REFERENCES groups(id),
    PRIMARY KEY (user_id, group_id)
);

-- child_id is nested in parent_id: members of child_id are members of parent_id.
CREATE TABLE group_nesting (
    child_id  INTEGER NOT NULL REFERENCES groups(id),
    parent_id INTEGER NOT NULL REFERENCES groups(id),
    PRIMARY KEY (child_id, parent_id)
);
CREATE INDEX group_nesting_parent ON group_nesting(parent_id);

CREATE TABLE grants (
    group_id    INTEGER NOT NULL REFERENCES groups(id),
    resource_id INTEGER NOT NULL REFERENCES resources(id),
    PRIMARY KEY (resource_id, group_id)
);
