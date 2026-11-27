The PRAC-SAT- practice trees are out of the training graph, and the PRAC-BASE course trees are untouched.

I ran `bin/tg run training scripts/remove_prac_sat.py`, which removes every node whose id starts with `PRAC-SAT-`. NetworkX drops each node's edges with it. Only the `training` target was changed. `published` was not touched.

- **Removed:** 41 PRAC-SAT trees, with their 41 `on_street` links and 101 `surveyed` links (142 edges).
- **Now in the graph:** 60 trees, 4 streets and 12 volunteers, with 60 `on_street` and 125 `surveyed` edges.

That is the same shape `scripts/build_training.py` describes for the course graph (4 streets, 60 PRAC-BASE trees, 12 volunteers). The volunteers and streets that Saturday's trees were linked to are still there, since they belong to the course.

The cleanup script is saved as `scripts/remove_prac_sat.py` in case you want to reuse it after the next session.
