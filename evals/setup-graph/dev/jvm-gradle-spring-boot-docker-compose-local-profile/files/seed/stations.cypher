CREATE (:Station {code: 'ST01', name: 'Ashby'}), (:Station {code: 'ST02', name: 'Bramwell'}),
       (:Station {code: 'ST03', name: 'Corfe Hill'}), (:Station {code: 'ST04', name: 'Dunmore'}),
       (:Station {code: 'ST05', name: 'Elsworth'});
MATCH (a:Station {code: 'ST01'}), (b:Station {code: 'ST02'}), (c:Station {code: 'ST03'}),
      (d:Station {code: 'ST04'}), (e:Station {code: 'ST05'})
CREATE (a)-[:CAN_LEND {appliance: 'aerial ladder', minutes: 18}]->(b),
       (b)-[:CAN_LEND {appliance: 'water carrier', minutes: 25}]->(c),
       (c)-[:CAN_LEND {appliance: 'aerial ladder', minutes: 31}]->(d),
       (a)-[:CAN_LEND {appliance: 'rescue tender', minutes: 22}]->(e),
       (e)-[:CAN_LEND {appliance: 'water carrier', minutes: 14}]->(d);
