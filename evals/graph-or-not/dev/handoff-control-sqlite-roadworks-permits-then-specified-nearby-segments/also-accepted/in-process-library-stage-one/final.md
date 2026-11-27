Added sql/nearby_segments.sql: a recursive walk over segments that share a junction, capped at :hops steps (so loops cannot run on), distinct segment ids, the start excluded.
