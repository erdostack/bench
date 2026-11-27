"""Sanity check run after the export lands: counts lines so the on-call can see a truncated export."""
from pathlib import Path


def count_lines(export_dir):
    d = Path(export_dir)
    accounts = sum(1 for line in open(d / "accounts.txt") if line.strip() and not line.startswith("#"))
    follows = sum(1 for line in open(d / "follows.edges") if line.strip() and not line.startswith("#"))
    return accounts, follows
