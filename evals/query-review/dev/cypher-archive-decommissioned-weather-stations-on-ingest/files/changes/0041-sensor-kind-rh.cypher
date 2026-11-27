// 0041: humidity sensors were loaded with kind 'humidity'; the API expects 'rh' (ticket MET-882).
MATCH (x:Sensor {kind: 'humidity'}) SET x.kind = 'rh';
