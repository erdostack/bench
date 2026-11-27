# Roast: pawprint model

I came here to roast a join table in a costume. It turns out the costume is a lab coat and the thing has a job.

## Findings

### 1. drug_recall (low)

**Problem.** For a drug that is prescribed a lot, this reads every prescription of it ever written and only then throws away the ones before $since. That is fine for something a person runs a few times a year; it would not be fine on a screen.

**Fix.** Leave it. If recalls ever become a button in the app, put the day on the PRESCRIBED relationship as well so old prescriptions can be skipped.

### 2. day_sheet (low)

**Problem.** Nothing wrong today: 550 visits a day come straight off the visit_day index and are then narrowed to one vet. Noting it only because it is the query that would change first if the group grew tenfold.

**Fix.** No change.

Verdict on Visit: keep it. Your lead is wrong on this one. A visit is the thing prescriptions hang off (which drug, what dose, how many days, at that visit) and the thing a re-check points back at. If you squash it into one line between an animal and a vet, there is nothing left for PRESCRIBED or FOLLOW_UP_OF to attach to, and an animal that sees the same vet twelve times becomes twelve parallel lines you have to tell apart by date. The model is fine to roll out.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
