CREATE TABLE image (
    id              INTEGER PRIMARY KEY,
    ref             TEXT NOT NULL,            -- registry/repo@sha256:...
    component_count INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE component (id INTEGER PRIMARY KEY, purl TEXT NOT NULL UNIQUE);
CREATE TABLE sbom_entry (image_id INTEGER NOT NULL REFERENCES image(id), purl TEXT NOT NULL, layer INTEGER NOT NULL);
CREATE TABLE image_component (
    image_id     INTEGER NOT NULL REFERENCES image(id),
    component_id INTEGER NOT NULL REFERENCES component(id)
);
CREATE INDEX sbom_entry_image ON sbom_entry(image_id);
CREATE INDEX image_component_image ON image_component(image_id);
CREATE INDEX image_component_component ON image_component(component_id);
