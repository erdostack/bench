CREATE TABLE relay (
    id        text PRIMARY KEY,
    role      text NOT NULL CHECK (role IN ('uplink', 'relay', 'client')),
    location  text
);

CREATE TABLE link (
    a        text NOT NULL REFERENCES relay (id),
    b        text NOT NULL REFERENCES relay (id),
    snr_db   real NOT NULL,
    seen_at  timestamptz NOT NULL,
    PRIMARY KEY (a, b)
);
