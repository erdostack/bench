# Model (written by the agency)

- `(:Client)-[:SIGNED]->(:Contract)-[:WITH]->(:Freelancer)`: a contract has its own rate, start and end,
  and collects `(:Milestone)`s, `(:Invoice)`s and, sometimes, a `(:Dispute)`.
- `(:Freelancer)-[:CLAIMS]->(:SkillClaim)-[:FOR_SKILL]->(:Skill)`: a freelancer's claim to a skill, with
  the year they started (`since`) and a self-rated `level` from 1 to 5. Nothing else points at a claim.
- `(:Freelancer)-[:LIVES_IN]->(:City)`.
