CREATE TABLE crash_report (
    id          BIGINT PRIMARY KEY,
    received_at TIMESTAMPTZ NOT NULL,
    app_version TEXT NOT NULL,
    device      TEXT NOT NULL,
    build       TEXT NOT NULL,
    signature   TEXT NOT NULL,          -- normalised top frames of the stack
    issue_id    BIGINT                  -- set by the grouping job
);

-- Two reports are linked when they share a stack signature, or the same device and build within a minute.
-- Written at intake; a report in a group of n gets up to n-1 links.
CREATE TABLE crash_link (
    a  BIGINT NOT NULL REFERENCES crash_report (id),
    b  BIGINT NOT NULL REFERENCES crash_report (id),
    why TEXT NOT NULL CHECK (why IN ('signature', 'device_build')),
    PRIMARY KEY (a, b)
);
CREATE INDEX crash_link_b ON crash_link (b);
