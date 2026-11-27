// CAT-2190: 37 toy categories were imported with upper-case slugs.
MATCH (c:Category)
WHERE c.slug STARTS WITH 'TOYS-'
SET c.slug = toLower(c.slug);
