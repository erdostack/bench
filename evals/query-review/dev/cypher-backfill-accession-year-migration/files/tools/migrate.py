"""Apply graph migrations in order.

    python3 tools/migrate.py --uri neo4j://localhost:7687 --user neo4j --password ...

Each file migrations/V<NNN>__<name>.cypher runs once; applied versions are recorded as
(:__Migration {version, appliedAt}).

By default a file runs inside one managed write transaction (session.execute_write), so a file that
fails leaves nothing behind. A file whose first line is exactly

    // migrate: autocommit

is instead run statement by statement, each statement as its own auto-commit query (session.run).
"""
import argparse
import re
from pathlib import Path

from neo4j import GraphDatabase

ROOT = Path(__file__).resolve().parent.parent
AUTOCOMMIT = "// migrate: autocommit"


def statements(text):
    """Statements of a file: split at a semicolon that ends a line; comment-only pieces are dropped."""
    out = []
    for piece in re.split(r";[ \t]*(?:\n|$)", text):
        code = [ln for ln in piece.splitlines() if ln.strip() and not ln.strip().startswith("//")]
        if code:
            out.append(piece.strip())
    return out


def applied(session):
    return {r["v"] for r in session.run("MATCH (m:__Migration) RETURN m.version AS v")}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--uri", required=True)
    ap.add_argument("--user", required=True)
    ap.add_argument("--password", required=True)
    args = ap.parse_args()
    driver = GraphDatabase.driver(args.uri, auth=(args.user, args.password))
    with driver.session() as session:
        done = applied(session)
        for path in sorted((ROOT / "migrations").glob("V*__*.cypher")):
            version = path.name.split("__")[0]
            if version in done:
                continue
            text = path.read_text()
            if text.splitlines()[0].strip() == AUTOCOMMIT:
                for st in statements(text):
                    session.run(st).consume()
            else:
                def work(tx):
                    for st in statements(text):
                        tx.run(st).consume()
                session.execute_write(work)
            session.run("CREATE (:__Migration {version: $v, appliedAt: datetime()})", v=version).consume()
            print("applied", path.name)
    driver.close()


if __name__ == "__main__":
    main()
