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
| 2 | Road one: the factory bakes the latest patches into a new base image | `README.md` pipeline (Base = GovTech + CIS hardening + packages + latest patches); `SPEC.md` S5 (base installs all updates, signed) | IMPLEMENTED |
| 3 | Road two: Patch Manager installs updates on running servers | patching issue record: Quick Setup patch policies and `AWS-RunPatchBaseline` associations | DOCUMENTED |
| 4 | A patch group is a tag on each server | patching issue record: policies target the `PatchGroup` tag | DOCUMENTED |
| 5 | Database servers, code-hosting servers and the backup host are separate groups | patching issue record: three group values, one per role | DOCUMENTED |
| 6 | Security updates are approved at once; other updates wait 7 days | patching issue record: the new baseline (security 0 days; bugfix, enhancement and others 7 days) | OWNER DIRECTION |
| 7 | By then the factory's image build has tested the same packages | `SPEC.md` S5 (base installs all updates) and the daily release rule | IMPLEMENTED |
| 8 | Database and container-engine packages are never patched in place | patching issue record: rejected packages in the new baseline | OWNER DIRECTION |
| 9 | They change only through a reviewed rolling upgrade or a new image | patching issue record, proposal D (owner-approved) | DOCUMENTED |
| 10 | Scans run on the weekend night; installs early next morning, each group in its own window | patching issue record: scan and install schedules per policy | OWNER DIRECTION |
| 11 | No automatic reboot; a new kernel takes effect at the next planned restart or image rollout | patching issue record: NoReboot on every install | DOCUMENTED |
| 12 | A policy installs only on servers whose tag matches; a mismatched server is scanned but never patched | patching issue record: lesson found and fixed (scan policy covers all production hosts; install policies cover only matching tags) | ILLUSTRATIVE (generic lesson; no host or count shown) |
| 13 | The daily and weekly reports list each server's patch result and flag "no patch data" | `monitoring/daily-summary/trust_prod_daily_ops_summary.py` (patch compliance), `monitoring/weekly.py` ("no patch data") | IMPLEMENTED |
| 14 | Every rule change is tried on one server first, then rolled out to every group | patching issue record: staged rollout (one host, then all groups) | OWNER DIRECTION |
| 15 | The owner approves every production change | `POLICY.md`; patching issue record | DOCUMENTED |

**Notes:**
- Every statement is generic: no account, host names, IDs, schedule times, dates or patch counts.
- The film claims no measured scan or install result; it explains how the flow works.
- The film shows only the three groups above; other server families are out of scope.
