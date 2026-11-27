Mostly sound. The one modelling mistake is SkillClaim: it's a relationship with two properties dressed
up as a node, and it puts an extra hop into your busiest query. Turn it into HAS_SKILL {since, level}.
Contract looks similar but is correct as a node: other things attach to it.
