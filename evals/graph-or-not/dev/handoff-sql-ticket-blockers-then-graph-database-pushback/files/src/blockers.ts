import pg from "pg";
import { load } from "./sql.js";

const pool = new pg.Pool({ connectionString: process.env.DATABASE_URL, max: 20 });
const BLOCKERS = load("blockers.sql");

export async function blockers(ticketId: number) {
  const { rows } = await pool.query(BLOCKERS, [ticketId]);
  return rows;
}
