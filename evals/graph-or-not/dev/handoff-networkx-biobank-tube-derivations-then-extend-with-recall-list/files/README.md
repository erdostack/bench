# tubetrack

Sample tracking for the cohort study's biobank: which tube came from which (aliquots, extractions, pools), where
each tube is, and the tools the lab uses when a consent is withdrawn or a reagent lot is recalled.

- Python 3.12, networkx. The tube data is a nightly export from the two lab systems (LIMS A for the main lab,
  LIMS B for the satellite lab) into `data/` (`tubes.csv`, `derivations.csv`).
- `tubetrack/graph.py` loads the derivations for the lineage plots.
