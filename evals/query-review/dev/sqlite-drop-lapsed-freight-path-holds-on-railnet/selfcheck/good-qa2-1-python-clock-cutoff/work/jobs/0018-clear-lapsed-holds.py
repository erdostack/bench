"""0018: clear lapsed holds (until before the first day of this month); open-ended holds stay."""
from datetime import date, datetime
import time
def run(conn):
    a = date.today().replace(day=1).isoformat()
    b = datetime.now().strftime('%Y-%m-01')
    c = time.strftime('%Y-%m-01')
    assert a == b == c, (a, b, c)
    total = 0
    while True:
        with conn:
            n = conn.execute("DELETE FROM edges WHERE id IN (SELECT id FROM edges WHERE kind = 'holds' AND until < ? LIMIT 1000)", (a,)).rowcount
        if not n:
            return total
        total += n
