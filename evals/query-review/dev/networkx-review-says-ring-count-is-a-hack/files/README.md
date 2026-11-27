# moldesc

Graph descriptors for the compound library (atoms are nodes, bonds are edges).

- `chem/descriptors.py`: the descriptors. `docs/descriptors.md` defines each one.
- `data/molecules.json`: the reference set the descriptors are checked against before each library release
  (`{"name": ..., "atoms": [...], "bonds": [[i, j, order], ...]}`; names are internal ids, not real compounds).
- `tests/`: `python3 -m pytest tests`.
