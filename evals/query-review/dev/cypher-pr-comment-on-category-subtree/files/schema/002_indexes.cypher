CREATE INDEX category_depth IF NOT EXISTS
FOR (c:Category) ON (c.depth);
