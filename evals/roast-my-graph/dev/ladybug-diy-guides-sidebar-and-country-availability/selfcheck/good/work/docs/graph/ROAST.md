# Review

It's the sidebar. related_guides fans out through every topic of the guide, and since the editors
tagged everything "general", one of those topics is attached to all 2.4 million guides. Exclude
general (or any huge topic) from that query or precompute the sidebar. The big US country isn't
an issue: you only ever go guide -> country.

## related_guides (critical)

Problem: Every guide now also points at the general topic, which has about 2.4 million guides. The sidebar query goes from this guide to each of its topics and back to every guide on them, so for general it pulls millions of rows, counts and sorts them, and only then keeps 5. That is the p95.

Fix: Leave general out of the walk: add WHERE t.slug <> 'general' (better, skip any topic with more than a few thousand guides), or stop recording general as an ABOUT row since it carries no information. If you want it richer, precompute the five related guides in the nightly job.

## AVAILABLE_IN (low)

Problem: US has 1.6 million rows, which looks alarming, but guide_countries only reads the handful of countries of one guide and nothing walks out of a country. Not a problem.

Fix: None needed.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
