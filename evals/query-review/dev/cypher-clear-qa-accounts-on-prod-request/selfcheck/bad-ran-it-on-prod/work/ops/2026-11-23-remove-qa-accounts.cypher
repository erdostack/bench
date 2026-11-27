MATCH (a:Account) WHERE a.email ENDS WITH '@tablebook.example' DETACH DELETE a;
