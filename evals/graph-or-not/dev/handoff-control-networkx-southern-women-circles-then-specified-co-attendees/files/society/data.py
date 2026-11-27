"""The study's attendance list."""
import csv
from pathlib import Path

DEFAULT = Path(__file__).resolve().parents[1] / "data" / "attendance.csv"


def load_attendance(path=DEFAULT):
    """[(woman, event), ...] as in the study."""
    with open(path, newline="", encoding="utf-8") as f:
        return [(row["person"], row["event"]) for row in csv.DictReader(f)]


def women(path=DEFAULT):
    return sorted({w for w, _ in load_attendance(path)})
