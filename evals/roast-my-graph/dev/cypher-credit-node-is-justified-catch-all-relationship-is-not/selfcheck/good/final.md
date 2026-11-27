docs/graph/ROAST.md and findings.json are written.

The thing to fix is RELATED. Spouse, sibling, parent, agent and 7.6M auto-generated frequent_collaborator links all share that one type and are told apart by a property, so the family and agent pages read every one of a person's RELATED relationships and discard nearly all of them. Give each kind its own type; I've sketched the loader and query changes.

Credit looks like a leftover link table but it is the right call: awards attach to a specific credit and acting credits point at a character, which a relationship could not do. Leave it.
