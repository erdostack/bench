# Roast: paperlib

Mostly fine, some modelling notes.

## Findings

### 1. Paper.venue (low)

**Problem.** Free-text venue.

**Fix.** Normalise if needed.

### 2. Journal.impact_factor (medium)

**Problem.** Impact factor is stored on the Journal node as a string.

**Fix.** Store it as DOUBLE.

### 3. [:PublishedIn] (medium)

**Problem.** PublishedIn has no year property.

**Fix.** Add one.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
