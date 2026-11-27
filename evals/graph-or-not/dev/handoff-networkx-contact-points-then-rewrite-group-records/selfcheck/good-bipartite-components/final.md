group_records now builds a record/contact graph from emails and phones only and returns the record ids of each
connected component, which is the rule in docs/graph/DECISION.md. All records are covered, singletons included.
