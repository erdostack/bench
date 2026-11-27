import { pool } from "../db";

const PAGE = 60;

const SQL = `
  SELECT a.id, a.title, a.taken_on
  FROM assets a
  WHERE a.id IN (
    SELECT at.asset_id
    FROM asset_tags at
    WHERE at.tag_id IN (SELECT expanded_tag_ids($1))
  )
  ORDER BY a.taken_on DESC
  LIMIT ${PAGE} OFFSET $2`;

export async function assetsByTag(tagId: number, page: number) {
  const { rows } = await pool.query(SQL, [tagId, page * PAGE]);
  return rows;
}
