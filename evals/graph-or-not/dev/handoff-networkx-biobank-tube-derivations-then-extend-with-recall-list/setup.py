"""Writes the biobank export (tubes.csv, derivations.csv) into data/ of the work dir."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import tubes_data  # noqa: E402

tubes_data.write(Path(sys.argv[1]) / "data")
