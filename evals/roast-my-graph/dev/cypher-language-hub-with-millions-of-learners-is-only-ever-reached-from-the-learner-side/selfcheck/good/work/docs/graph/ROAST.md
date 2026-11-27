# Roast: parlo graph

Checked every statement for which side of the Language hub it starts from.

## Findings

### 1. language_totals (low)

**Problem.** Counts every SPEAKS and LEARNING relationship (about 21 million) each night. That is the size of the question, not a modelling problem, and it is nowhere near the app's peak path.

**Fix.** Run it off-peak as now. If the page ever needs live numbers, keep a counter per Language updated by set_learning.

### 2. finish_lesson (low)

**Problem.** Keeps every finish as its own FINISHED relationship, so a Lesson ends up with millions of them, like Language. Same answer: nothing reads them by starting from the lesson, and next_lessons uses the position on ENROLLED_IN instead.

**Fix.** Nothing for now. If the streak calendar ever needs old history fast, it reads from the learner side, which is already the case.

### 3. Language (low)

**Problem.** The consultant's concern. Language has millions of incoming relationships, but every hot query reaches it from the learner or course side and none expands out of it, so it does not slow anything down.

**Fix.** Keep one node per language. Re-check only if a new feature starts from a Language and lists its learners (for example a 'find a partner' search); that one would need a different design.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
