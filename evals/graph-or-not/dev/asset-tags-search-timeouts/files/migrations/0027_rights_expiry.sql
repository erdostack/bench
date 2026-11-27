ALTER TABLE assets ADD COLUMN rights_expire_on date;
CREATE INDEX assets_rights_expire_idx ON assets (rights_expire_on) WHERE rights_expire_on IS NOT NULL;
