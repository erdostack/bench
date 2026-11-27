It feels clunky because the schema is still the MySQL one. Two findings, both high, in docs/graph/ROAST.md and findings.json:

1. CrewAssignment is a table whose only job is to connect a sailor to a vessel. Make it a relationship table from Sailor to Vessel with role and the two dates on it.
2. Voyage is not connected to anything: its ports and vessel are text codes. Add relationship tables to Port and Vessel and the two voyage queries stop comparing strings across 900k rows.

I gave the CREATE REL TABLE statements for both.
