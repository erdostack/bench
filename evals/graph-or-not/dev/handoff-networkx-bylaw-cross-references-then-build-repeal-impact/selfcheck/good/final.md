Rewrote affected_by_repeal in bylaws/impact.py as recorded in docs/graph/DECISION.md: networkx ancestors of
the bylaw over `amends` and `depends_on` references only, at any depth, so a citation carries nothing and
there is no level cap any more. networkx needs installing where the site runs.
