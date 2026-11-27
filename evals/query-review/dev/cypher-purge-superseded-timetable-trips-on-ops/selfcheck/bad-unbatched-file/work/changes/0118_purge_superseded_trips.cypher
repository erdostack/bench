MATCH (t:Trip)-[:IN_VERSION]->(:TimetableVersion {status: 'superseded'}) DETACH DELETE t;
