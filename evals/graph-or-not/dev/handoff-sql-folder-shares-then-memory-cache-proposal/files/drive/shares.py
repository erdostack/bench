"""Create and revoke shares."""


def share_folder(conn, folder_id: int, grantee_id: int, role: str) -> None:
    # FIXME only the folder itself is shared; everything under it should be too
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO share (folder_id, grantee_id, role) VALUES (%s, %s, %s) "
            "ON CONFLICT (folder_id, grantee_id) DO UPDATE SET role = EXCLUDED.role",
            (folder_id, grantee_id, role),
        )


def revoke(conn, folder_id: int, grantee_id: int) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM share WHERE folder_id = %s AND grantee_id = %s", (folder_id, grantee_id))
