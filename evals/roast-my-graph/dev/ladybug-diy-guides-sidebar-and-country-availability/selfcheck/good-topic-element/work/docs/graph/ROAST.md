# Review

The 'general' topic is a hub every sidebar query walks through. Exclude it.

## ABOUT to Topic 'general' (high)

Problem: A topic attached to every guide turns related_guides into a scan of the whole catalogue for each page view.

Fix: Remove the general ABOUT rows (keep the editors' flag as a Guide column if needed) or filter t.slug <> 'general' in related_guides, as topic_page already does.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
