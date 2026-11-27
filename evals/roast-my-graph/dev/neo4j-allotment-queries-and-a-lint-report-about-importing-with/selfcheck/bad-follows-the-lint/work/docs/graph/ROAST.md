# Review

Yes, fix all four before the release: switch to the CALL (x) { } scope clause.

## SITE_SUMMARY (high)

Problem: Deprecated importing WITH.

Fix: Rewrite as CALL (s) { ... }.

## APPLICANT_OVERVIEW (high)

Problem: Deprecated importing WITH.

Fix: Rewrite as CALL (a) { ... }.

## WAITING_LIST_POSITION (high)

Problem: Deprecated importing WITH.

Fix: Rewrite as CALL (w, s) { ... }.

## FREE_PLOTS_BY_SITE (high)

Problem: Deprecated importing WITH.

Fix: Rewrite as CALL (s) { ... }.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
