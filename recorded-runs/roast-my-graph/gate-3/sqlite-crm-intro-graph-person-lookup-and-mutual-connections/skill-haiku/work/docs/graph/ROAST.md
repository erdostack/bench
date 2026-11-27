# Roast: introgate schema, queries and sidebar API

Verdict: The graph part is innocent: mutual_connections.sql is two primary-key searches and stays fast. The budget is blown by the email lookup in person_by_email.sql, which scans all 1.2 million people on every sidebar request because lower(email) cannot use the index on email. One high finding, one low question.

Judged against:
- SQLite, version not stated in the repo; intro.db was last written by SQLite 3.53.1
- 1.2 million people, 9 million knows rows, p95 budget 80 ms per sidebar request, README.md
- 30 teams, README.md
- Emails arrive in whatever case the CRM stored them, README.md
- knows is stored in both directions, the loader writes a row each way, README.md
- The sample intro.db has 60,000 people and 480,722 knows rows, README.md and intro.db

## Findings

### high: `person_by_email.sql`
The lookup is the same shape as a phone book page sorted by the wrong column. Every sidebar request reads the whole book before it can say whose number it is.
Problem: The sidebar's email lookup filters on lower(email) = lower(:email). The UNIQUE index on person.email is case-sensitive and cannot serve a lower() expression, so every sidebar request scans the whole person table. The plan on the sample is SCAN person. Scaled to the stated 1.2 million people, the scan is about 144 ms on this machine (measured 7.2 ms per lookup on the 60,000-row sample, times 20, a linear estimate), against an 80 ms p95 budget. Every contact open hits it.
Fix: `CREATE INDEX person_email_lower ON person (lower(email));`. SQLite 3.53.1 then plans the query as SEARCH person USING INDEX person_email_lower. Verified in memory on a copy of intro.db: identical results for 200 sampled emails, mixed-case input still matches, and the per-lookup time falls to about 0.004 ms. Make it UNIQUE only after checking production for case-variant duplicates; the sample has none.

### low: `email`
Two spellings of one address are allowed by the constraint and ignored by the lookup. That is a question, not yet a bug.
Problem: person.email is UNIQUE and case-sensitive, but the lookup ignores case. If the CRM stores two spellings of one address as two people, person_by_email returns both rows and fetchone() keeps an arbitrary one, with no ORDER BY to choose. The README says emails arrive in whatever case the CRM stored them. The sample has no such pairs, so this is a question to confirm.
Fix: Confirm whether production can hold two people whose emails differ only in case. If it can, decide which person wins and say so in the query, or normalise email to lower case on load so the UNIQUE constraint covers it.

## Holds up
- `mutual_connections.sql`: both joins are primary-key searches. The plan on the sample is SEARCH k1 USING PRIMARY KEY (a=?), SEARCH k2 USING PRIMARY KEY (a=? AND b=?), and a rowid search on person. The mutual query took about 0.012 ms on the sample. Per person there are about 7.5 knows rows (9 million over 1.2 million), so the sort is over a handful of rows. It would change if a person had thousands of contacts.
- `knows` stored in both directions: in the 480,722 sample rows there is no row without its reverse and no strength that differs between the two directions. The mutual query relies on this, so it holds only while the loader keeps writing both rows; the loader is not in the repo.
- `knows` key and checks: PRIMARY KEY (a, b) with WITHOUT ROWID, strength BETWEEN 1 AND 5, and CHECK (a <> b). The composite key serves lookups by a, which is the direction the query uses.
- `team_by_name.sql`: lower(name) scans 30 team rows on the admin settings page. The table is tiny and the path is rare, so the scan is sound.
- `person.team_id`: has no index, but no query in the repo filters on it, so there is nothing to serve.

## Not checked
- The 144 ms figure is a linear estimate from a 60,000-row sample on this machine, not a measurement at 1.2 million people. Production is the only place to confirm it.
- The loader is not in the repo, so whether it writes both knows directions, and whether it normalises email case, cannot be checked.
- Production was not available, so duplicates by case cannot be ruled out there. The sample has none.
- The full API call was timed on the sample at about 7 ms, dominated by the email scan.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
