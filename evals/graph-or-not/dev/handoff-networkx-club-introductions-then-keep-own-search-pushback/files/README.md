# clubhouse

Members' app for sports clubs: rosters, sessions, and "who can introduce me", which shows a chain of members
who know each other, from you to someone you'd like to meet.

- Python 3.12, Flask. `requirements.txt`.
- Production data lives in the platform's Postgres; each club is loaded into memory per request from its
  `tie` rows (a tie = two members who train together).
- Test data: `data/ties.csv`, Zachary's karate club network (34 members, 78 ties; the copy bundled with
  networkx as `karate_club_graph`). Members are numbered 0 to 33.
- `pytest` runs the tests.
