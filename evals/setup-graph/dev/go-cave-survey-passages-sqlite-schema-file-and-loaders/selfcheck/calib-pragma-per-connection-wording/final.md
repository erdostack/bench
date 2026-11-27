Recorded. PRAGMA foreign_keys is per connection, and only initdb's connection sets it, so the FK constraints are inert for load/merge; foreign_key_check reports orphaned passages already.
