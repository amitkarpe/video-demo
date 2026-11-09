# Evidence map — "Patching Running Servers in AWS Factory"

Each on-screen or spoken statement, mapped to the private source (`amitkarpe/aws-factory` @ `0808975` and its patching issue record, read-only). Public-safe: categories only, no IDs, host names, schedule times, dates or counts.

**States:**
- **IMPLEMENTED:** in code or configuration that the source shows.
- **DOCUMENTED:** an approved, recorded configuration or decision; not re-measured here.
- **ILLUSTRATIVE:** a teaching picture, not a measurement.
- **OWNER DIRECTION:** the owner directed (9 Nov 2026) that the film presents this as the working flow, in generic terms. This file does not re-measure it.

| # | Statement (film) | Source | State |
|---|---|---|---|
| 1 | New security fixes for Amazon Linux arrive regularly | general fact | ILLUSTRATIVE |
| 2 | Road one: the factory bakes the latest patches into a new image | `README.md` pipeline (Base = GovTech + CIS hardening + packages + latest patches); `SPEC.md` S5 | IMPLEMENTED |
| 3 | Road two: Patch Manager installs updates on running servers | patching issue record: patch policies and `AWS-RunPatchBaseline` | DOCUMENTED |
| 4 | One hardened base image, and from it three families: GitLab, MongoDB, the CloudOS workspace on ECS | `README.md` pipeline (Base → ECS, MongoDB, GitLab images) | IMPLEMENTED |
| 5 | Each server's tag names its family; that tag is its patch group | patching issue record: policies target the `PatchGroup` tag, one value per family | OWNER DIRECTION |
| 6 | Each family has its own rules and its own time slot | patching issue record: one patch policy per family, each with its own install slot | OWNER DIRECTION |
| 7 | Security updates are approved at once; other updates wait 7 days | patching issue record: the baseline rules | OWNER DIRECTION |
| 8 | By then the factory's image build has tested the same packages | `SPEC.md` S5 (base installs all updates) and the release rule | IMPLEMENTED |
| 9 | Database and container-engine packages are never patched in place; they change through a reviewed rolling upgrade or a new image | patching issue record: rejected packages; owner-approved proposal | OWNER DIRECTION |
| 10 | Every weekend night Patch Manager scans each group | patching issue record: weekend scan policy | OWNER DIRECTION |
| 11 | If nothing is missing, the group is compliant and nothing else happens | Patch Manager behaviour (an install run with nothing missing installs nothing) | DOCUMENTED (AWS behaviour) |
| 12 | Missing updates install early next morning in the group's own window, one group after another | patching issue record: per-family install slots | OWNER DIRECTION |
| 13 | Most installs need no reboot; a new kernel's reboot waits for the group's planned downtime window | patching issue record: installs run with NoReboot; owner direction (a reboot only in the predefined downtime) | OWNER DIRECTION |
| 14 | A policy installs only on servers whose tag matches; a mismatched server is scanned but never patched | patching issue record: a lesson found and fixed | ILLUSTRATIVE (generic lesson; no host or count shown) |
| 15 | The daily and weekly reports list each server's patch result and flag "no patch data" | `monitoring/daily-summary/trust_prod_daily_ops_summary.py`, `monitoring/weekly.py` | IMPLEMENTED |
| 16 | Every rule change is tried on one server first, then rolled out to every group | patching issue record: staged rollout | OWNER DIRECTION |
| 17 | The owner approves every production change | `POLICY.md`; patching issue record | DOCUMENTED |

**Notes:**
- Every statement is generic: no account, host names, IDs, schedule times, dates or patch counts.
- The film claims no measured scan or install result; it explains how the flow works.
- Which family needs a reboot and which has nothing missing (CloudOS and MongoDB in the film) is ILLUSTRATIVE: it shows the three possible outcomes, not a real run.
