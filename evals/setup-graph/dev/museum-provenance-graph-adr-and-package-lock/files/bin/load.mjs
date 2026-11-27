// Rebuild var/provenance.lbdb from data/*.csv.
import { readFileSync, rmSync, mkdirSync } from 'node:fs';
import { open } from './db.mjs';

rmSync('var', { recursive: true, force: true });
mkdirSync('var');
const conn = open({ readOnly: false });
for (const statement of readFileSync('schema/schema.cypher', 'utf8').split(';')) {
  if (statement.trim()) await conn.query(statement);
}
await conn.query("COPY Holder FROM 'data/holders.csv' (header=true)");
await conn.query("COPY Item FROM 'data/items.csv' (header=true)");
await conn.query("COPY HELD FROM 'data/held.csv' (header=true)");
