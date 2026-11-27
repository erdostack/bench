Decision: no-graph. Written up in docs/graph/DECISION.md.

The rules stop at level 2: the referrer and the referrer's referrer. However long the chains get (26 is the longest
you have found), the bonus job reads two rows up `member.referred_by` per new member, about 4,000 times on a busy
night, out of 1.3M members, with the index that is already there. Nothing here needs a traversal, a graph database or
a graph library; two self-joins on MariaDB do it.
