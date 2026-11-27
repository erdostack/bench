Added `dependents_within` to `depgraph/impact.py`: a recursive CTE over `depends_on` bounded by `max_hops`, grouped to the minimum hop count. Unit test added and passing on the tiny graph.
