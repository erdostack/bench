CREATE TABLE speaker (
    id     INTEGER PRIMARY KEY,
    name   TEXT NOT NULL,
    email  TEXT NOT NULL
);

-- starts_at is local time, ISO 8601 ("2026-05-12T09:30").
CREATE TABLE session (
    id         INTEGER PRIMARY KEY,
    title      TEXT NOT NULL,
    room       TEXT NOT NULL,
    starts_at  TEXT NOT NULL
);

CREATE TABLE session_speaker (
    session_id  INTEGER NOT NULL REFERENCES session (id),
    speaker_id  INTEGER NOT NULL REFERENCES speaker (id),
    PRIMARY KEY (session_id, speaker_id)
);

CREATE TABLE tag (
    id    INTEGER PRIMARY KEY,
    name  TEXT NOT NULL UNIQUE
);

CREATE TABLE session_tag (
    session_id  INTEGER NOT NULL REFERENCES session (id),
    tag_id      INTEGER NOT NULL REFERENCES tag (id),
    PRIMARY KEY (session_id, tag_id)
);

-- One row each time a speaker checks in at the speaker desk; checked_in_at is local time, ISO 8601.
CREATE TABLE speaker_checkin (
    speaker_id     INTEGER NOT NULL REFERENCES speaker (id),
    checked_in_at  TEXT    NOT NULL
);
