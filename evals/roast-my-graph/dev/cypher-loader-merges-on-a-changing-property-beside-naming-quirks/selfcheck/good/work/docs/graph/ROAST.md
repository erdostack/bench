# Roast: postroom graph

Most of this file is a perfectly ordinary loader. One line of it has been quietly cloning your customers every night, like a photocopier with a grudge.

## Findings

### 1. load_subscribers (critical)

**Problem.** The statement looks for a subscriber with this email AND this plan. The night after someone moves from free to monthly there is no such node, so a brand-new Subscriber is created next to the old one, with the same email. load_subscriptions and load_opens then find both by email and attach everything to both. audience_size counts that person twice, and that is the number advertisers are invoiced on. With 3% of 2.4 million people changing plan a month, that is tens of thousands of extra subscribers every month, and it never heals.

**Fix.** Match on the email only and write the plan afterwards: MERGE (s:Subscriber {email: row.email}) SET s.plan = row.plan, s.name = row.name, s.country = row.country, s.joined_on = date(row.joined_on). Then clean up: for each email with more than one node, keep one and delete the rest, and re-run the load. After that, turn subscriber_email into a uniqueness constraint so it cannot come back.

### 2. subscriber_email (medium)

**Problem.** Email is the only thing that identifies a subscriber, and nothing says it has to be unique: it is a plain index.

**Fix.** Make it a uniqueness constraint, after the duplicates are gone. On its own it would not fix the loader; it would make the nightly load fail instead of duplicating.

### 3. partOf (low)

**Problem.** Every other relationship type is written LIKE_THIS; this one is camelCase. The loader and recent_issues agree with each other, so nothing is broken, it just trips people writing new queries.

**Fix.** Rename to PART_OF in load_issues and recent_issues together, when convenient.

### 4. Issue.SentAt (low)

**Problem.** Same story: the only property that starts with a capital. Used consistently.

**Fix.** Rename to sent_at at the same time.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
