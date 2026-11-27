// 0032: keeper RFT was renamed Railfreight Leasing on 2026-09-01 (keeper notice KN-118).
MATCH (k:Keeper {code: 'RFT'}) SET k.name = 'Railfreight Leasing';
