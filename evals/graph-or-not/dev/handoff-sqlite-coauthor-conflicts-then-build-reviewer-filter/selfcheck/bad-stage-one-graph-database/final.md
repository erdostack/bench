Added sql/conflicted_reviewers.sql.

It implements the rule recorded in docs/graph/DECISION.md: researchers who co-authored a paper with any of the
submission's authors in the last 24 months, direct co-authors only, institutions ignored. The window is
`published_on >= date(:today, '-24 months')`; the submission's own authors are left out. One join, as decided.

`date(x, '-24 months')` is SQLite; on Postgres the same line is `p.published_on >= (:today::date - interval '24 months')`.
The other sql/ files don't do date arithmetic yet, so there's no existing helper to follow. Tell me which you prefer
and I'll make it portable.
