"""Monday batch: letters for applications received in the past week."""
from datetime import date, timedelta


def weekly_letters(conn, today: date) -> list[dict]:
    since = today - timedelta(days=7)
    apps = conn.execute(
        "SELECT a.id, a.parcel_id, p.cadastre FROM application a JOIN parcel p ON p.id = a.parcel_id "
        "WHERE a.received >= %s AND a.received < %s ORDER BY a.id", (since, today)).fetchall()
    letters = []
    for app_id, parcel_id, cadastre in apps:
        # TODO: one letter per owner of an adjacent parcel (planning bylaw)
        pass
    return letters
