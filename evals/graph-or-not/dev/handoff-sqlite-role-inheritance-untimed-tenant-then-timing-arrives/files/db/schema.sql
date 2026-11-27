CREATE TABLE tenant (id INTEGER PRIMARY KEY, name TEXT NOT NULL);

CREATE TABLE role (
  id        INTEGER PRIMARY KEY,
  tenant_id INTEGER NOT NULL REFERENCES tenant(id),
  name      TEXT NOT NULL
);

-- role_id inherits everything parent_role_id has.
CREATE TABLE role_inherits (
  role_id        INTEGER NOT NULL REFERENCES role(id),
  parent_role_id INTEGER NOT NULL REFERENCES role(id),
  PRIMARY KEY (role_id, parent_role_id)
);
CREATE INDEX role_inherits_parent ON role_inherits(parent_role_id);

CREATE TABLE role_permission (
  role_id    INTEGER NOT NULL REFERENCES role(id),
  permission TEXT NOT NULL,
  PRIMARY KEY (role_id, permission)
);

CREATE TABLE user_role (
  user_id INTEGER NOT NULL,
  role_id INTEGER NOT NULL REFERENCES role(id),
  PRIMARY KEY (user_id, role_id)
);
CREATE INDEX user_role_role ON user_role(role_id);
