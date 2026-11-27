"""python -m coverage.run <network.json>: print the referral table as JSON."""
import json
import sys

from coverage.load import clinics, load_roads
from coverage.nearest import nearest_clinics

if __name__ == "__main__":
    G = load_roads(sys.argv[1])
    table = nearest_clinics(G, clinics(G))
    json.dump({v: table[v] for v in sorted(table)}, sys.stdout, indent=1)
