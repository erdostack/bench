One thing to fix before the report: institute_collaboration doubles the pair count, because it
matches COAUTHORED in both directions while the loader stores each pair once. Add the arrow. The
undirected coauthors query is right as it is (a researcher can be either end), and LINK_PAIR's two
lookups are single rows. Details in docs/graph/ROAST.md and findings.json.
