Position: keep

Lena, we decided to run both checks in CI with networkx over the quest YAML (tools/validate.py), and the reasons were
specific:

- The graph is about 22k quests and 61k prerequisite edges, and the data the check needs is the YAML in the PR itself.
- The prototype runs in 1.8 s including parsing. We get about 40 content PRs a day; that is a minute of CI a day.
- We have no ops team and nobody on call. A graph database is a server someone has to run, upgrade and wake up for,
  and it would still have to be loaded from each PR's YAML before CI could ask it anything.

The dependency browser is a good idea in its own right, and it can read the same YAML. It is not a reason to move the
checks.
