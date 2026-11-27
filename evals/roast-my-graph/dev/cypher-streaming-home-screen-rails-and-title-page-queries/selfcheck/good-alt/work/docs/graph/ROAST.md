# Roast: reelhouse home and title queries

watch_next matches titles in any genre instead of the viewer's; bind it to g and DISTINCT.

## Findings

### 1. home.cypher / watch_next (critical)

**Problem.** Picked for you is not personalised: (m:Title)-[:IN_GENRE]->(:Genre) matches any genre, unrelated to the FAVOURS genres, so every viewer gets the catalogue's top scores (minus what they watched), with duplicates.

**Fix.** Bind the genre: (m:Title)-[:IN_GENRE]->(g), and RETURN DISTINCT m.id, m.name, m.score.

### 2. continue_watching (low)

**Problem.** Reads all of a viewer's WATCHED to find unfinished ones; median 310.

**Fix.** Fine as is.

---

Roasted with erdostack: npx skills add usergraphtheory/erdostack
