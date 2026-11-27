# Roast: reelbase model

I saw a node wedged between Person and Production and reached for the flamethrower. Then I read what hangs off it and put the flamethrower down. The real mess is one relationship that has been asked to mean five things, one of which a script writes 7.6 million times.

## Findings

### 1. RELATED (medium)

**Problem.** Five different things share one relationship name and are told apart by a `kind` property: spouse, sibling, parent, agent, and frequent_collaborator. The last one is machine-generated and makes up 7.6 million of the 9 million. So the family page and the agent page pick up every RELATED relationship a person has, almost all of them collaborators, read `kind` on each one, and throw nearly everything away. For someone with a long career that is thousands of relationships inspected to find one spouse.

**Fix.** Give each kind its own relationship type, so the database can go straight to the right ones: SPOUSE_OF, SIBLING_OF, PARENT_OF, REPRESENTED_BY and COLLABORATES_WITH. In load_related, route rows by kind (one statement per kind, or FOREACH with a CASE filter). family becomes MATCH (p)-[r:SPOUSE_OF|SIBLING_OF|PARENT_OF]-(q) RETURN q.name, type(r), and represented_by becomes MATCH (p)-[r:REPRESENTED_BY]->(agent). At the very least move frequent_collaborator out to its own type.

### 2. Credit (low)

**Problem.** A node sitting between Person and Production usually means someone could not let go of a link table. I checked whether this one earns its place and it does: an Award points at a single credit (HONOURS), an acting credit points at a Character (PLAYS), and one person can hold several credits on one production. A relationship cannot be pointed at by an award or point at a character, so collapsing Credit into a Person-to-Production relationship would lose the two pages the site depends on.

**Fix.** Keep it as a node. No change.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
