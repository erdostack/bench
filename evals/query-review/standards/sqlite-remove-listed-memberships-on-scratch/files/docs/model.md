# Model

See `db/schema.sql`.

- A forum's members are the rows of `has_member` (`forum_id`, `person_id`, `join_date`). A forum's moderator is
  `forum.moderator_id`; a moderator is normally a member as well, but the two are separate.
- `knows` holds each friendship once (`person1_id` sent the request).
- `post.forum_id` is the forum a post is in; `comment.reply_of` is the message it answers.
- Dates are TEXT, `'YYYY-MM-DD HH:MM:SS'`, UTC.
