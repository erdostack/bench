import { pool } from "./db.js";

export interface Profile {
  id: number;
  name: string;
  gradYear: number;
  programme: string;
  connections: number;
}

export async function profile(viewerId: number, memberId: number): Promise<Profile | null> {
  const { rows } = await pool.query(
    `SELECT m.id, m.name, m.grad_year, m.programme,
            (SELECT count(*) FROM connection c WHERE c.member_id = m.id) AS connections
       FROM member m WHERE m.id = $1`,
    [memberId],
  );
  if (rows.length === 0) return null;
  const r = rows[0];
  // TODO: "N mutual connections" line with the first few names (viewerId vs memberId)
  return { id: r.id, name: r.name, gradYear: r.grad_year, programme: r.programme, connections: Number(r.connections) };
}
