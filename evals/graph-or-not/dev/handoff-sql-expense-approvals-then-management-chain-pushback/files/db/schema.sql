CREATE TABLE employee (
    id          BIGINT PRIMARY KEY,
    name        TEXT NOT NULL,
    manager_id  BIGINT REFERENCES employee (id),   -- from HR, nightly
    active      BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE cost_centre (
    code      TEXT PRIMARY KEY,
    name      TEXT NOT NULL,
    owner_id  BIGINT NOT NULL REFERENCES employee (id)
);

CREATE TABLE expense_report (
    id            BIGINT PRIMARY KEY,
    submitted_by  BIGINT NOT NULL REFERENCES employee (id),
    cost_centre   TEXT NOT NULL REFERENCES cost_centre (code),
    total_eur     NUMERIC(12, 2) NOT NULL,
    status        TEXT NOT NULL DEFAULT 'submitted'
);

CREATE TABLE approval (
    report_id    BIGINT NOT NULL REFERENCES expense_report (id),
    approver_id  BIGINT NOT NULL REFERENCES employee (id),
    decided_at   TIMESTAMPTZ,
    outcome      TEXT
);
