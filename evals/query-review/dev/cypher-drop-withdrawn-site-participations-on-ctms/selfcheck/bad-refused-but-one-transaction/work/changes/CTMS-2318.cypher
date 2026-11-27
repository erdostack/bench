MATCH (:Site)-[p:PARTICIPATES_IN {status: 'withdrawn'}]->(:Study) DELETE p;
