-- hearth: members and friendships. SQLite.

-- Account states, maintained by trust & safety. See the rows in the table itself.
CREATE TABLE account_state (
    code   INTEGER PRIMARY KEY,
    label  TEXT NOT NULL UNIQUE
);

CREATE TABLE person (
    id             INTEGER PRIMARY KEY,
    first_name     TEXT NOT NULL,
    last_name      TEXT NOT NULL,
    gender         TEXT,
    birthday       TEXT,
    creation_date  TEXT NOT NULL,
    location_ip    TEXT,
    browser_used   TEXT,
    state          INTEGER NOT NULL DEFAULT 1 REFERENCES account_state(code)
);

-- A friendship, stored once: person1_id is always the smaller id.
CREATE TABLE person_knows_person (
    person1_id     INTEGER NOT NULL REFERENCES person(id),
    person2_id     INTEGER NOT NULL REFERENCES person(id),
    creation_date  TEXT NOT NULL,
    PRIMARY KEY (person1_id, person2_id),
    CHECK (person1_id < person2_id)
);

CREATE INDEX person_knows_person_2 ON person_knows_person(person2_id);
