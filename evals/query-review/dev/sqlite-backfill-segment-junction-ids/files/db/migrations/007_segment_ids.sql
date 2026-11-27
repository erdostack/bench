ALTER TABLE segments ADD COLUMN from_id INTEGER REFERENCES junctions(id);
ALTER TABLE segments ADD COLUMN to_id INTEGER REFERENCES junctions(id);
