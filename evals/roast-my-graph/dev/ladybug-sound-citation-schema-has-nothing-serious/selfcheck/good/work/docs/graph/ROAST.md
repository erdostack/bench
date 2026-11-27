# Roast: paperlib

I came to roast and the kitchen is clean. Three node tables with real keys, three relationship tables pointing the right way, byline order stored on the relationship it describes, and nothing the app asks for that the keys cannot find. Annoying. Two small things, neither urgent.

## Findings

### 1. Paper.venue (low)

**Problem.** Venue is free text on each paper, so "NeurIPS" and "Neural Information Processing Systems" are two different venues as far as any query can tell.

**Fix.** Leave it until someone wants to browse by venue. If they do, add a Venue node table keyed by a normalised name and a PublishedIn relationship table from Paper to Venue.

### 2. Cites (low)

**Problem.** Nothing stops the weekly import from recording the same citation twice, which would double-count it in "cited together" lists.

**Fix.** Have the import skip a (citing, cited) pair it has already written. Nothing to change in the table definition.

Verdict: nothing here needs fixing before you get on with your week.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
