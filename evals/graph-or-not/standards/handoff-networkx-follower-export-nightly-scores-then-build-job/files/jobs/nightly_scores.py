"""Nightly scores job: reach and ring for every account (docs/scores.md).

Run from cron after the export lands: python3 -m jobs.nightly_scores exports/
"""
import sys

# TODO: compute reach and ring for every account in the export, then hand them to the loader (separate ticket).

if __name__ == "__main__":
    print("not implemented yet:", sys.argv[1:])
