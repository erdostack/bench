#!/usr/bin/env python3
"""scripts/seed.py: print a tiny CSV sample (twenty objects) for demos. Writes to stdout, touches no database."""
import csv
import random
import sys

MEDIA = ["oil on panel", "bronze", "salt-glazed stoneware", "silver", "woodcut", "linen"]


def main() -> None:
    rng = random.Random(1887)
    writer = csv.writer(sys.stdout)
    writer.writerow(["accession", "title", "date_made", "medium"])
    for number in range(1, 21):
        writer.writerow([f"DEMO.{number:03d}", f"Untitled study {number}", str(rng.randint(1620, 1930)), rng.choice(MEDIA)])


if __name__ == "__main__":
    main()
