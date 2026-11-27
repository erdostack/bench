"""Nightly report: who can reach each sensitive system."""
import csv
import sys
from pathlib import Path

import networkx as nx

from review.load import load

SENSITIVE = ["payroll", "treasury", "hr-records", "prod-db-admin"]


def who_can_reach(g, system):
    return sorted(n[1] for n in nx.ancestors(g, ("system", system)) if n[0] == "identity")


def main(export_dir, out_dir):
    g = load(export_dir)
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for system in SENSITIVE:
        with open(Path(out_dir) / f"{system}.csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["identity_id"])
            w.writerows([i] for i in who_can_reach(g, system))


if __name__ == "__main__":
    main(*sys.argv[1:3])
