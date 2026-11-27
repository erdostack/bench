"""Load the nightly knowledge-base dump."""
import pickle
from pathlib import Path

DUMP = Path(__file__).resolve().parent.parent / "data" / "kb.pkl"


def load(path=DUMP):
    with open(path, "rb") as handle:
        return pickle.load(handle)
