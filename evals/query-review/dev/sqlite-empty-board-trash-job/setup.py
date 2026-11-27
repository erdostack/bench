"""Build var/pinboard.db: 50,000 cards on 900 boards (about 6% in the trash since before 2026-10-24, 5%
trashed later), ~85,000 connectors, ~30,000 frame memberships. Connectors were trashed with their card,
and some were restored on their own afterwards."""
import random
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

work = Path(sys.argv[1])
db = work / "var" / "pinboard.db"
db.parent.mkdir(parents=True, exist_ok=True)
if db.exists():
    db.unlink()
rng = random.Random(2410)
conn = sqlite3.connect(db)
conn.executescript((work / "db" / "schema.sql").read_text())
N = 50000
cards, board_of, trashed = [], {}, {}
for i in range(1, N + 1):
    b = rng.randint(1, 900)
    board_of[i] = b
    kind = rng.choices(["note", "image", "link", "frame"], [6, 2, 1, 1])[0]
    t = None
    u = rng.random()
    if u < 0.06:
        t = datetime(2026, 7, 1) + timedelta(seconds=rng.randint(0, 114 * 86400))     # before 2026-10-23
    elif u < 0.11:
        t = datetime(2026, 10, 24, 1) + timedelta(seconds=rng.randint(0, 29 * 86400))
    trashed[i] = t.strftime("%Y-%m-%d %H:%M:%S") if t else None
    cards.append((i, b, kind, "2026-01-05 10:00:00", trashed[i]))
conn.executemany("INSERT INTO cards VALUES (?, ?, ?, ?, ?)", cards)
by_board = {}
for i, b in board_of.items():
    by_board.setdefault(b, []).append(i)
conns = []
for b, ids in by_board.items():
    for _ in range(len(ids) * 17 // 10):
        x, y = rng.sample(ids, 2)
        t = trashed[x] or trashed[y]
        if trashed[x] and trashed[y]:
            t = min(trashed[x], trashed[y])
        if t and rng.random() < 0.18:
            t = None                               # arrow restored on its own after its card was trashed
        if not t and not trashed[x] and not trashed[y] and rng.random() < 0.01:
            t = "2026-11-%02d 12:00:00" % rng.randint(10, 22)   # an arrow deleted by itself, recently
        conns.append((x, y, rng.choice([None, None, "depends on", "next", "see"]), t))
conn.executemany("INSERT INTO connectors (from_card, to_card, label, trashed_at) VALUES (?, ?, ?, ?)", conns)
frames = [c[0] for c in cards if c[2] == "frame"]
members = set()
for f in frames:
    for m in rng.sample(by_board[board_of[f]], min(len(by_board[board_of[f]]), rng.randint(2, 8))):
        if m != f:
            members.add((f, m))
conn.executemany("INSERT INTO frame_members VALUES (?, ?)", sorted(members))
conn.execute("ANALYZE")
conn.commit()
conn.close()
