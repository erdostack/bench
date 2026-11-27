# Model

| node kind | code | notes |
|---|---|---|
| `device` | `MD-012345` | `class` (`anaesthesia`, `infusion`, `monitor`, `ventilator`, ...) and `status` |
| `ward` | `W-ICU1` | |
| `vendor` | `V-HALVARD` | manufacturers |
| `contract` | `SC-2027-ANA` | service contracts |

Device `status`: `in_service`, `in_store` (ours, kept as a spare), `loan` (lent to us by a vendor or
another trust), `condemned` (withdrawn, waiting for disposal).

| edge kind | src | dst | `since` |
|---|---|---|---|
| `located_in` | device | ward | date it moved there |
| `made_by` | device | vendor | |
| `covered_by` | device | contract | date the cover starts (`YYYY-MM-DD`) |
