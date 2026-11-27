import { Database, Connection } from '@ladybugdb/core';

export function open({ readOnly = true } = {}) {
  const db = new Database('var/provenance.lbdb', { readOnly });
  return new Connection(db);
}
