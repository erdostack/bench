Added sql/conflicted_reviewers.sql as a single join, per docs/graph/DECISION.md.

A conflict is co-authorship with any of the submission's authors in the last 36 months, the standard window for
journal conflicts of interest. The submission's own authors are excluded.
