# Claims map: ops sample (52 s)

Every on-screen or spoken claim, its label and its source in `amitkarpe/nextflow-offline` (main 356ed30, read 10 Nov 2026 SGT).

| Time | Claim | Label | Source |
|---|---|---|---|
| 0-8 s | A researcher asks whether a run was offline | Illustrative | Story device; no real message |
| 8-15 s | GitLab (the runner) prepares the release once | Implemented | `docs/cloud-operations.md`, GitLab `prepare:<lane>` jobs |
| 15-20 s | Bundle in private S3, SHA-256 for every file | Implemented | SPEC.md bundle contract, `check-bundle` stage |
| 20-24 s | Images in private ECR, locked by digest | Implemented | Skopeo copy by digest, `check-images` stage |
| 24-28 s | Host has no route to the internet (no NAT, IGW or public IP) | Dated evidence, 5 Nov 2026 SGT | `docs/cloud-operations.md` line 108, `docs/validation-host.md` |
| 28-31 s | Only private AWS endpoints (S3, ECR, SSM) reach it | Implemented | `docs/bootstrap.md` (S3 gateway and interface endpoints) |
| 32-40 s | A task that reaches out is blocked; stage 8 `offline-execute` fails; RESULT=FAIL | Illustrative drill | Podman `--network none --pull=never` (AGENTS.md rules); stage names from the CodePipeline |
| 41-44 s | PASS means all 10 stages passed | Implemented | CodePipeline `nextflow-offline-dev-ops`, 10 stages |
| 41-48 s | Sarek PASS | Dated evidence, 3 Nov 2026 SGT | AGENTS.md, execution 43ecb80c |
| 44-48 s | Evidence: run report, digests, checksums, no-route probe | Implemented / dated | `expected_output` = `results/pipeline_info/execution_report_*.html` |
| 48-52 s | Offline emulation, not a physical air gap | Required caveat | AGENTS.md rules |

Not shown on purpose: GitHub, account IDs, instance IDs, hostnames, project IDs.
