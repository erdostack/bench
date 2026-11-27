upstream() is in deploytool/impact.py, following ADR 0012: I keep the edges seen on at least 3 of the last 7 days and walk callers with a visited set, since the call graph has cycles.

Checked on a toy db with 6 services and a callback pair: 4 names back, and it returns.
