-- Postgres, owned by the flags admin service.
CREATE TABLE flag (
  key         text PRIMARY KEY,
  description text NOT NULL,
  rollout     jsonb NOT NULL,          -- targeting rules
  updated_at  timestamptz NOT NULL
);

-- A flag is on for a user only if every prerequisite is on (in the given variation) for that user.
CREATE TABLE flag_prerequisite (
  flag_key     text NOT NULL REFERENCES flag(key),
  requires_key text NOT NULL REFERENCES flag(key),
  variation    text NOT NULL DEFAULT 'on',
  PRIMARY KEY (flag_key, requires_key)
);
