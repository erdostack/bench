MATCH (c:Contract {status: 'cancelled'}) DETACH DELETE c;
