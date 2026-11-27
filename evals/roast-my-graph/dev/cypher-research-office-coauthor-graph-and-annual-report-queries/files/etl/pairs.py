"""Publications export -> one row per pair of staff coauthors: {first, second, papers}, first < second."""
import csv
import itertools
import json
import sys
from collections import Counter


def pairs(rows):
    authors_by_paper = {}
    for row in rows:
        authors_by_paper.setdefault(row["paper_id"], set()).add(row["orcid"])
    shared = Counter()
    for authors in authors_by_paper.values():
        for first, second in itertools.combinations(sorted(authors), 2):
            shared[(first, second)] += 1
    return [{"first": a, "second": b, "papers": n} for (a, b), n in sorted(shared.items())]


if __name__ == "__main__":
    with open(sys.argv[1], newline="") as fh:
        json.dump(pairs(csv.DictReader(fh)), sys.stdout)
