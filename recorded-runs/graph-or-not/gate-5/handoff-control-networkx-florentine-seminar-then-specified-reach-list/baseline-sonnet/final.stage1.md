Decision: in-process-library

Use networkx, which the app already has. With 16 families and 20 ties that never change, the reach count is a breadth-first search over a graph that fits in a few hundred bytes. Neo4j would be a server to install, run and keep in sync for 25 students, and it would be slower and more fragile than the 3 lines it replaces. If students should learn a graph database, that can be a separate exercise on a larger dataset. The reach panel doesn't need it. Recursive SQL would also work, but it is harder to read and to explain to students than a BFS call.

What I did: I replaced the TODO in `seminar/app.py` with `GET /api/families/<name>/reach`.
- It loads the families and marriage ties from SQLite, then runs `nx.single_source_shortest_path_length` with a cutoff of 3.
- It returns `{"family", "within": {1, 2, 3}, "exactly": {1, 2, 3}}`.
- `within` counts other families reachable through at most k marriages. `exactly` counts those exactly k marriages away. The panel can show whichever fits your wording.
- An unknown family gives 404.

Check: I built the DB and called the endpoint with the Flask test client. Medici gives within 1, 2 and 3 of 6, 11 and 14 (14 is every other family that has any tie). Pucci, who has no ties, gives 0, 0 and 0. An unknown name gives 404. I removed the generated `var/` folder afterwards and added no test file.

Note for the seminar: the Pucci were added as an isolated family, so their panel shows zero at every step. That is the correct result and worth explaining to students.
