CREATE TABLE tags (
    id    serial PRIMARY KEY,
    name  text NOT NULL UNIQUE
);

CREATE TABLE asset_tags (
    asset_id  bigint  NOT NULL REFERENCES assets (id),
    tag_id    integer NOT NULL REFERENCES tags (id),
    PRIMARY KEY (asset_id, tag_id)
);
