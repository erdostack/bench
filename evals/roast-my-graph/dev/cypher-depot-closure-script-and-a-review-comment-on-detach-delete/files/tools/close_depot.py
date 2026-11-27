"""Close a depot: python -m tools.close_depot LEEDS-02 LEEDS-01"""
import pathlib
import sys

from neo4j import GraphDatabase

STATEMENTS = [s.strip() for s in pathlib.Path("graph/closure.cypher").read_text().split(";") if s.strip()]


def close(tx, closing, target):
    if closing == target:
        raise ValueError("closing and target must differ")
    for statement in STATEMENTS[:2]:
        tx.run(statement, closing=closing, target=target).consume()
    closed = tx.run(STATEMENTS[2], closing=closing, target=target).single()["closed"]
    if closed != 1:
        raise RuntimeError(f"{closing} still has stock or staff; nothing was deleted")


def main(closing, target, uri="neo4j://graph.internal:7687"):
    with GraphDatabase.driver(uri) as driver, driver.session(database="network") as session:
        session.execute_write(close, closing, target)


if __name__ == "__main__":
    main(*sys.argv[1:3])
