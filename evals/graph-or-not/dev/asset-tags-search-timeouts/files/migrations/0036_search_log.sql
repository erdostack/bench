CREATE TABLE search_log (
    id           bigserial PRIMARY KEY,
    searched_at  timestamptz NOT NULL DEFAULT now(),
    tag_id       integer,
    duration_ms  integer,
    cancelled    boolean NOT NULL DEFAULT false
);
