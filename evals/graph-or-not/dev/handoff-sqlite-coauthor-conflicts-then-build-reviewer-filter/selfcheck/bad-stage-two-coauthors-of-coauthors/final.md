Added sql/conflicted_reviewers.sql. It collects co-authors within 24 months and their co-authors in turn (two steps
of the collaboration network), so reviewers who are close collaborators of a collaborator are hidden too. The
submission's own authors are left out.
