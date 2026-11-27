import { readFileSync } from "node:fs";
import pg from "pg";

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL });
const SEE_ALSO = readFileSync(new URL("../sql/see_also.sql", import.meta.url), "utf8");

export async function seeAlso(articleId: number) {
  return (await pool.query(SEE_ALSO, [articleId])).rows;
}
