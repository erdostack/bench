"""Answer the door controllers."""


def may_open(conn, badge_id: int, door_id: int) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM door d JOIN badge_zone bz ON bz.zone_id = d.zone_id "
            "WHERE d.id = %s AND bz.badge_id = %s",
            (door_id, badge_id),
        )
        return cur.fetchone() is not None
