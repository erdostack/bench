CREATE TABLE owner (
    id       BIGINT PRIMARY KEY,
    name     TEXT NOT NULL,
    address  TEXT NOT NULL
);

CREATE TABLE parcel (
    id        BIGINT PRIMARY KEY,
    cadastre  TEXT   NOT NULL UNIQUE,
    owner_id  BIGINT NOT NULL REFERENCES owner (id),
    geom      geometry(MultiPolygon, 25832) NOT NULL
);

-- Written nightly by the GIS team: one row per ordered pair of parcels whose boundaries touch.
CREATE TABLE parcel_adjacency (
    parcel_id    BIGINT NOT NULL REFERENCES parcel (id),
    neighbour_id BIGINT NOT NULL REFERENCES parcel (id),
    PRIMARY KEY (parcel_id, neighbour_id)
);

CREATE TABLE application (
    id         BIGINT PRIMARY KEY,
    parcel_id  BIGINT NOT NULL REFERENCES parcel (id),
    kind       TEXT   NOT NULL,
    received   DATE   NOT NULL,
    status     TEXT   NOT NULL
);
