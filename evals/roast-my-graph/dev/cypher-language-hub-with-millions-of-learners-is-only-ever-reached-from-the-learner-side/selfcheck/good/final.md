He's wrong for this app, and nothing in graph/ needs fixing before launch.

A node with millions of relationships only hurts when a query starts there and walks out through them. None of the peak queries does: profile, learner_home, next_lessons and finish_lesson all start from one learner and follow that learner's few relationships, arriving at a Language at the end, which costs the same as arriving at any node. course_list starts from the 930 courses. Splitting Language per country would make profile and set_learning more awkward and speed up nothing.

The one statement that does read all of English's relationships is the nightly language_totals, and that's because its answer really is "count all of them". I noted it as low, with two other small notes, in docs/graph/ROAST.md and findings.json.
