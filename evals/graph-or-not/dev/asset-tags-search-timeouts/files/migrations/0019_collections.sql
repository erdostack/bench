CREATE TABLE collections (
    id          serial PRIMARY KEY,
    title       text NOT NULL,
    created_by  integer NOT NULL
);

CREATE TABLE collection_assets (
    collection_id  integer NOT NULL REFERENCES collections (id),
    asset_id       bigint  NOT NULL REFERENCES assets (id),
    position       integer NOT NULL,
    PRIMARY KEY (collection_id, asset_id)
);
