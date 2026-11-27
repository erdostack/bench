export function log(scope, message, extra = {}) {
  console.log(JSON.stringify({ at: new Date().toISOString(), scope, message, ...extra }));
}

export function requireEnv(name) {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is not set`);
  return value;
}
