-- linkup core schema (PostgreSQL 16).

CREATE TABLE person (
    id             bigint PRIMARY KEY,
    first_name     text NOT NULL,
    last_name      text NOT NULL,
    gender         text,
    birthday       date,
    creation_date  timestamptz NOT NULL,
    location_ip    inet,
    browser_used   text,
    city_id        bigint
);

-- One row per friendship, stored once: person1_id < person2_id.
CREATE TABLE knows (
    person1_id     bigint NOT NULL REFERENCES person(id),
    person2_id     bigint NOT NULL REFERENCES person(id),
    creation_date  timestamptz NOT NULL,
    PRIMARY KEY (person1_id, person2_id),
    CHECK (person1_id < person2_id)
);

CREATE INDEX knows_person2 ON knows (person2_id, person1_id);
