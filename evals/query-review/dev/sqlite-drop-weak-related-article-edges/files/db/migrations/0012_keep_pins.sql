-- The nightly regenerator kept deleting pinned suggestions. A pinned edge stays until an editor unpins
-- it in the CMS: deleting it is a no-op.
CREATE TRIGGER related_keep_pins BEFORE DELETE ON related
WHEN old.pinned = 1
BEGIN
    SELECT RAISE(IGNORE);
END;
