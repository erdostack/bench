// Parameters: $slug, $name
MATCH (c:City {slug: $slug})
SET c.name = $name;
