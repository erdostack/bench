# Roast: morgue schema

A schema with no indexes walks into a newsroom.

## Findings

### 1. Tag (critical)

**Problem.** No secondary index on Tag.slug or Article.published; every tag lookup is a full scan.

**Fix.** Add indexes on Tag.slug, Article.published and Person.staff_no.

### 2. TaggedWith (high)

**Problem.** Polymorphic relationship table pointing from two different node tables; queries cannot rely on the source type.

**Fix.** Split into ArticleTaggedWith and EpisodeTaggedWith.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
