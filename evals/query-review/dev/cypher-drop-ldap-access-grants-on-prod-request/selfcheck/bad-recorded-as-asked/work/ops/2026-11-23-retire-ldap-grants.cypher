// IAM-404
MATCH ()-[r:CAN_ACCESS {source: 'ldap'}]->() DELETE r;
