# registry-impact

The "what breaks if I yank this" check for the internal package registry. The publish CLI calls it before a yank
or a deprecation goes through and waits for the answer.

- Python 3.12, FastAPI. MySQL 8.0 is the registry's database (owned by the registry team).
- `impact/reverse.py` computes every version that depends, directly or transitively, on a given version.
