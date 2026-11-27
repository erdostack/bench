CREATE TABLE centre (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    kind TEXT NOT NULL CHECK (kind IN ('depot', 'hub', 'office'))
);

CREATE TABLE leg (
    from_code TEXT NOT NULL REFERENCES centre(code),
    to_code   TEXT NOT NULL REFERENCES centre(code),
    cost_pence INTEGER NOT NULL,
    PRIMARY KEY (from_code, to_code)
);
