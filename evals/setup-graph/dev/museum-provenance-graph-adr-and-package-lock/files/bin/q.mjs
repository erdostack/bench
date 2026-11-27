// npm run q -- <file.cypher> [object id]
import { readFileSync } from 'node:fs';
import { open } from './db.mjs';

const [file, objectId] = process.argv.slice(2);
const conn = open({ readOnly: true });
const prepared = await conn.prepare(readFileSync(file, 'utf8'));
const result = await conn.execute(prepared, objectId ? { id: objectId } : {});
console.table(await result.getAll());
