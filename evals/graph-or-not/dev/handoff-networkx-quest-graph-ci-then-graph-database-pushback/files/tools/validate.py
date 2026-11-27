"""Checks run on every content PR. Each check returns a list of problems."""
import sys
from pathlib import Path

import yaml

CONTENT = Path(__file__).resolve().parents[1] / "content" / "quests"


def load():
    return {d["id"]: d for d in (yaml.safe_load(p.read_text()) for p in CONTENT.rglob("*.yaml"))}


def missing_requirements(quests):
    return [f"{q['id']} requires unknown {r}" for q in quests.values() for r in q.get("requires", []) if r not in quests]


# TODO: unreachable quests and prerequisite loops (designers keep shipping both)
CHECKS = [missing_requirements]


def main():
    quests = load()
    problems = [p for check in CHECKS for p in check(quests)]
    print("\n".join(problems) or "ok")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
