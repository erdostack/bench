Decision: no-graph

This is one join on the tables you already have, not a graph problem. Reasoning in docs/graph/DECISION.md.

The rule looks exactly one step out: co-authors of the submission's authors on papers from the last 24 months.
Nothing walks further, so there is no traversal to speed up. With an index on authorship.researcher_id, finding a
few authors' recent papers and their co-authors out of 5.2M authorship rows is milliseconds, far inside the second
the picker has, at 1,800 submissions a month. A graph database would mean copying 310k researchers and 1.4M papers
into a second store every week for that one join. Collaboration networks are a textbook graph, but this rule only
ever uses the first ring of it.
