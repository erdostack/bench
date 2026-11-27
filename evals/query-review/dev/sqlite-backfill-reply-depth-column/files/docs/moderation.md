# Moderation

- **Lock** a thread: no new replies (`threads.locked = 1`).
- **Hide** a post: `posts.hidden = 1`; it stays in the tree, its replies stay visible.
- **Merge** a thread into another: the moved thread's first post gets a `parent_id` (the post in the
  target thread it now answers), so the whole moved thread hangs under that post. Its `thread_id`
  is rewritten to the target thread.
- **Close stale threads**: done by the nightly job, not by hand.
