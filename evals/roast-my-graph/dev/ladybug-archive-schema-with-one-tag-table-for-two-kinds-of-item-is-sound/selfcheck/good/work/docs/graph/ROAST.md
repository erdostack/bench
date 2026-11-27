# Roast: morgue schema

Asked to be thorough and honest. Read with docs/decisions.md and LadybugDB's own DDL rules in mind.

## Findings

### 1. related_tags (medium)

**Problem.** For a big tag (tens of thousands of articles) it reads every tag of every one of those articles, a few hundred thousand rows, before counting. Fine for a desk tool, but it is the slowest query here.

**Fix.** If it becomes annoying, precompute co-occurrence counts in the nightly import, or limit it to recent articles.

### 2. Article.slug (low)

**Problem.** Nothing says a slug is unique, so a pasted URL could in principle return two articles. article_by_slug is a full scan of Article, as docs/decisions.md says, and takes about a second.

**Fix.** Have the import reject a duplicate slug; leave the scan as it is unless the desk starts to mind.

### 3. TaggedWith (low)

**Problem.** Not a defect: one relationship table with two FROM/TO pairs is valid LadybugDB DDL and fits one tag vocabulary for both kinds of item. Mentioned only because it was questioned.

**Fix.** Keep it.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
