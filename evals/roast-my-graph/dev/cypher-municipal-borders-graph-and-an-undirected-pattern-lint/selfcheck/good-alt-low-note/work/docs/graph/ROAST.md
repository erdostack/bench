# Review

The three CL204 warnings are false positives: anchored, guarded with a.code < b.code, and halved.
Nothing needs to change; I noted one optional rewrite.

## total_border_km.cypher (low)

Correct (the /2 undoes the two orientations), but a directed pattern says the same thing without the arithmetic.

Fix: Optional: MATCH (:Municipality)-[r:BORDERS]->(:Municipality) RETURN sum(r.length_km).

Roasted with erdostack: npx skills add usergraphtheory/erdostack
