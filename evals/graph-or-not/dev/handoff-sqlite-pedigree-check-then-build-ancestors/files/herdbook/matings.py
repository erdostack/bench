"""Mating submissions."""
from . import sqlfile


def submit(conn, sire_id: int, dam_id: int, today: str) -> int:
    # TODO common-ancestor check before a mating is accepted (inbreeding rule)
    cur = conn.cursor()
    cur.execute("INSERT INTO mating (sire_id, dam_id, submitted_on) VALUES (:s, :d, :t)",
                {"s": sire_id, "d": dam_id, "t": today})
    return cur.lastrowid


def offspring(conn, animal_id: int):
    return sqlfile.run(conn, "offspring", animal_id=animal_id)
