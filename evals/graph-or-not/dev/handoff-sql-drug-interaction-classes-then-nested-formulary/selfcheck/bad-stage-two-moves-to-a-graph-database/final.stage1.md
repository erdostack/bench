Decision: no-graph

There is no traversal here. Every drug has exactly one class and the class list is flat, so a rule applies to a pair
of drugs when it names either drug or either drug's class: one join from the prescription and the patient's current
medicines to interaction_rule. You measured it at 4 ms p95 on a copy of prod against the 200 ms the check has, at
about 3,000 checks a minute, on 21k drugs and 140k rules. A graph database would be a monthly copy of the vendor's
formulary for that join. Written down in docs/graph/DECISION.md.
