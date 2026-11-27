"""Build var/fleet.db as last night's crash left it: 25,000 sensors (ids 1001-26000), 15,500 of them in a
ring, rings.member_count missing chunk 29 (sensors 15001-15500)."""
import sqlite3
import sys
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "fleet.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
conn.executemany("INSERT INTO devices VALUES (?, ?, 'gateway', NULL)", [(i, f"GW-{i:05d}") for i in range(1, 301)])
conn.executemany("INSERT INTO devices VALUES (?, ?, 'sensor', ?)",
                 [(i, f"SN-{i:07d}", f"cust-{i % 70:03d}") for i in range(1001, 26001)])
conn.executemany("INSERT INTO rings VALUES (?, ?, 0)", [(1, "canary"), (2, "early"), (3, "broad")])


def ring(i):
    return 1 if i % 20 == 0 else 2 if 1 <= i % 20 <= 4 else 3


conn.executemany("INSERT INTO ring_members VALUES (?, ?)", [(i, ring(i)) for i in range(1001, 15501)])
for rid in (1, 2, 3):
    conn.execute("UPDATE rings SET member_count = ? WHERE id = ?", (sum(1 for i in range(1001, 15001) if ring(i) == rid), rid))
conn.commit()
conn.close()
