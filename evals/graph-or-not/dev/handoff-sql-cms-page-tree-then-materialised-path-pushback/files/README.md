# newsroom-cms

Editorial CMS for the publishing group's sites. TypeScript, Node 22, Postgres 16 via `postgres` (porsager).

- Pages form a tree per site (`page.parent_id`). Sections are pages with children.
- `src/tree/` holds everything that reads the tree: section listings, sitemaps, permission inheritance.
