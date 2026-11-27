// GB-201: one collection per slug.
CREATE CONSTRAINT collection_slug IF NOT EXISTS FOR (c:Collection) REQUIRE c.slug IS UNIQUE;
