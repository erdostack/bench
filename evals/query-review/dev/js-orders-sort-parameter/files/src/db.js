'use strict';
const neo4j = require('neo4j-driver');

function makeDriver() {
  const uri = process.env.NEO4J_URI || 'neo4j://localhost:7687';
  const user = process.env.NEO4J_USERNAME || 'neo4j';
  return neo4j.driver(uri, neo4j.auth.basic(user, process.env.NEO4J_PASSWORD));
}

module.exports = { makeDriver };
