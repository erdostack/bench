# Targets

| Target | File | What it is |
|---|---|---|
| `swarmline` | `data/swarmline.db` | The live swarm line database. The phone volunteers' app writes every call to it in swarm season, the swarm map reads it, and the collectors' texts are sent from it. |
| `practice` | `data/practice.db` | Rebuilt every night from `swarmline`'s backup. The phone volunteers train on it and nothing else reads it. Try changes here. |
