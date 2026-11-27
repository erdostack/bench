import { pool } from "./db";

// May `userId` act on `resourceId` with `role`?
// Looks at grants to the user and to groups the user is a direct member of.
export async function check(userId: string, resourceId: string, role: string): Promise<boolean> {
  const { rowCount } = await pool.query(
    `SELECT 1
       FROM grant_ g
      WHERE g.resource_id = $2
        AND g.role = $3
        AND (g.principal_id = $1
             OR g.principal_id IN (SELECT group_id FROM membership WHERE member_id = $1))
      LIMIT 1`,
    [userId, resourceId, role],
  );
  return (rowCount ?? 0) > 0;
}
