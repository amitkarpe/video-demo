# Evidence map — "CIS Hardening in AWS Factory" (Phase 1 draft)

**Source:** `amitkarpe/aws-factory` @ `080897512f33ab8c375995413add7ee8d882d013` (private, read-only). Paths are relative to that repository.

**Public-output rule.** This repository is public, so the film and this map stay at the category level:
- no CIS control numbers
- no credential or password details
- no account, instance or image IDs
- no dates

The exact control list lives only in the private source.

**States:**
- **IMPLEMENTED:** code does this.
- **DOCUMENTED:** the source docs state it.
- **DEMONSTRATED:** recorded evidence shows it.
- **ILLUSTRATIVE:** made for the film.

| # | Claim | State | Source | Line |
|---|---|---|---|---|
| 1 | The CIS Benchmark for Amazon Linux 2023 has 243 checks across Level 1 and Level 2 | DOCUMENTED | `docs/RUNBOOK.md` (Tenable CIS AL2023 v1.0.0 L1 and L2 audit files: 243 controls) | s02 |
| 2 | Not every control is fixed, by decision | DOCUMENTED | issue #9 ("we do not aim for 100% hardening") | s03 |
| 3 | CIS is the Center for Internet Security; Level 1 is essential settings, Level 2 is stricter defence in depth | External (public CIS definitions) | cisecurity.org benchmark profile definitions | s04–s05 |
| 4 | Line: GovTech parent → base (CIS fixes, agents, patches) → ECS, MongoDB, GitLab images → test → share | IMPLEMENTED | `README.md` pipeline; `release/release.py` | s07–s08 |
| 5 | The line runs on a new parent image or new patches (and at least every 28 days) | IMPLEMENTED | `README.md` (EventBridge rule) | s09 |
| 6 | Many controls arrive hardened by the GovTech parent image | DOCUMENTED | issue #9 ("GovTech already hardens", refs #4) | s11 |
| 7 | The base image fixes login lockout and password rules, file and log permissions, audit rules, unused networking and package-source signature checks | IMPLEMENTED | `images/base/50-cis-fixes.yml`; `images/base/30-os-audit-rules.yml`; `images/base-runtime.yml.tftpl` (`ApplyObservedCISCorrections`, repository signature check) | s12 |
| 8 | A small set is accepted risk with the owner's approval: five separate-partition controls and one user start-up-file permission control (six in total) | IMPLEMENTED + DOCUMENTED | `release/release.py` `ACCEPTED_CONTROLS`; `POLICY.md` §Exceptions (approved by the owner, not by Security or TISO) | s13–s16 |
| 9 | Accepted controls are named in code, so they are visible and reviewable | IMPLEMENTED | `release/release.py` `ACCEPTED_CONTROLS` | s17 |
| 10 | Each release reboots the base test host, then runs a CIS Level 2 scan, plus HCR checks | IMPLEMENTED + DOCUMENTED | `docs/RUNBOOK.md` (reboot before scan); `README.md` (Test stage); `release/probes/hcr.py` | s19 |
| 11 | A failure that is not on the approved list stops the release | IMPLEMENTED | `POLICY.md` §Exceptions; `release/release.py` | s20 |
| 12 | Scanner FAILED labels are never changed | DOCUMENTED | `POLICY.md` §Exceptions; `README.md` | s21 |
| 13 | The 243-square grid and the bucket cards | ILLUSTRATIVE | made for the film | slides 1, 4 |

**Deliberately not said:**
- the individual control numbers
- one further accepted risk that concerns a credential setting (kept private)
- that Security or TISO approved the exceptions
- "100% compliant"
- any PROD detail
