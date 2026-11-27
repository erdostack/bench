CREATE TABLE terminal (
    id      INTEGER PRIMARY KEY,
    code    TEXT NOT NULL UNIQUE,
    name    TEXT NOT NULL,
    region  TEXT NOT NULL
);

-- a lane is a directed, scheduled linehaul edge between two terminals
CREATE TABLE lane (
    id             INTEGER PRIMARY KEY,
    from_terminal  INTEGER NOT NULL REFERENCES terminal(id),
    to_terminal    INTEGER NOT NULL REFERENCES terminal(id),
    carrier        TEXT NOT NULL,
    weekly_loads   INTEGER NOT NULL,
    last_run_on    TEXT NOT NULL,          -- ISO date of the last dispatched load
    status         TEXT NOT NULL CHECK (status IN ('active', 'dormant', 'closed'))
);
CREATE INDEX lane_from ON lane(from_terminal);
CREATE INDEX lane_to ON lane(to_terminal);
CREATE INDEX lane_status ON lane(status);
