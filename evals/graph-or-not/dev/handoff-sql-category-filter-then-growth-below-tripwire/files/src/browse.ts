import type { Pool } from "pg";
import { sql } from "./sql.js";

const subtree = sql("category_subtree");

export async function browse(pool: Pool, categoryId: number, limit = 48) {
  const { rows } = await pool.query(subtree, [categoryId, limit]);
  return rows;
}
