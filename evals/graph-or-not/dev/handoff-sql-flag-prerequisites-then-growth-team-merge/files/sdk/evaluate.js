// SDK side (shared by web and mobile): evaluate a flag for a user from the downloaded snapshot.
export function evaluate(snapshot, key, user, seen = new Set()) {
  const flag = snapshot.flags[key];
  if (!flag) return "off";
  if (seen.has(key)) return "off";          // the admin UI rejects loops; belt and braces
  seen.add(key);
  for (const req of flag.requires) {
    if (evaluate(snapshot, req.flag, user, seen) !== req.variation) return "off";
  }
  return matchRollout(flag.rollout, user);
}

function matchRollout(rollout, user) {
  return rollout.default ?? "off";
}
