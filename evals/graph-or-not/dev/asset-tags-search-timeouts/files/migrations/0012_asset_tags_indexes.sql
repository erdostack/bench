-- Tag search was scanning asset_tags from the asset side.
CREATE INDEX asset_tags_tag_id_idx ON asset_tags (tag_id, asset_id);
