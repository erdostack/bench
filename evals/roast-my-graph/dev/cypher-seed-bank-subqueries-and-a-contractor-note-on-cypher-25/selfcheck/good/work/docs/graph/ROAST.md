# Review

He's wrong. `CALL (b) { }` arrived in Neo4j 5.23, not with Cypher 25, and both your compose file and
the helm values pin 5.26, so these queries run fine. If anything, his suggested `CALL { WITH b ... }`
is the form that's deprecated on 5.26. Keep them. One low note on the alerts report.

## viability_alerts (low)

Problem: Reads every germination test of the past year (tens of thousands) and filters them one by one; fine for a weekly report, not for a page someone waits on.

Fix: Keep it as a report; if it moves to a page, store a pass/fail flag when the test is recorded.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
