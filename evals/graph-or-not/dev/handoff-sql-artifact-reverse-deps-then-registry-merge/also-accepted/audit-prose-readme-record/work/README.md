# registry-impact

The "what breaks if I yank this" check for the internal package registry. The publish CLI calls it before a yank
or a deprecation goes through and waits for the answer.

- Python 3.12, FastAPI. MySQL 8.0 is the registry's database (owned by the registry team).
- `impact/reverse.py` computes every version that depends, directly or transitively, on a given version.

## Reverse-dependency check

Decision (revised after the registry merge): graph database. Earlier decision: in-process library.

The rule: in-process while the graph fits in half a 32 GB host. 21 GB at 33M edges is over 16 GB.
