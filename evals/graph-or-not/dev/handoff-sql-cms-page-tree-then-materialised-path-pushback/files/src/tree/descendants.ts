import type { Sql } from "postgres";

// TODO: everything under a section (listings, sitemaps, permission inheritance). Today only direct children.
export async function children(sql: Sql, pageId: number) {
  return sql`SELECT id, slug, title FROM page WHERE parent_id = ${pageId} ORDER BY slug`;
}
