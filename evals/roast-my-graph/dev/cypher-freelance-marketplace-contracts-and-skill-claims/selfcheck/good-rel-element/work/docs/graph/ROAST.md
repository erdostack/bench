# Review

Skill claims should be relationships, not nodes. Everything else holds up.

## CLAIMS / FOR_SKILL (high)

Problem: Two relationships plus a node where one relationship with properties would do; the search walks Skill <- SkillClaim <- Freelancer for every hit.

Fix: Replace the pair with -[:HAS_SKILL {level, since}]-> between Freelancer and Skill.

Roasted with erdostack: npx skills add usergraphtheory/erdostack
