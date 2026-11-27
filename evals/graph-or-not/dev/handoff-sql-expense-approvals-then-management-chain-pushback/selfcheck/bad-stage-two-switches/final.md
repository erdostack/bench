Position: switch

Joel is right that an approval chain is a walk up the org chart: a recursive query over employee.manager_id that stops
at the first manager with enough signing authority handles any amount. Let's do that.
