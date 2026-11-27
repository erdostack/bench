MATCH ()-[r:REFERRED {source: 'vendor-test'}]->()
DELETE r;
