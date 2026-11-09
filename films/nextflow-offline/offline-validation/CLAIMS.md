# Evidence map — "Nextflow Offline: Prepare Once, Run with Confidence"

**Source:** `amitkarpe/nextflow-offline` @ `356ed30f322a109788ca68f352961a33a7bba046` (private, read-only), plus the owner's direction for this film (Issue #765 in that repository and the owner's chat instructions of 9 Nov 2026). Paths below are relative to that repository. This map is for reviewers. None of it appears in the film.

**Film language rule (owner direction).**
- The film describes one confident, working flow in generic, high-level language.
- No code, scripts, file names, commands, fingerprint values, commit or run IDs, account, instance, host or project IDs, and no dates.
- GitLab is the only repository service shown or named. Other development services are never named or depicted.
- No "proposed" or status badges. The only on-screen tag is *Illustration*, on the two reconstructed moments.

**States** (playbook §6.1, plus one for this film):
- **IMPLEMENTED**: code at the revision does this.
- **DEMONSTRATED**: recorded run evidence at the revision shows it.
- **DOCUMENTED**: the source docs describe it.
- **OWNER DIRECTION**: stated as working by the owner for this film. It is the owner's description of the solution and goes beyond what the revision shows. Reviewers should check these rows.
- **ILLUSTRATIVE**: a reconstructed moment, tagged *Illustration* on screen.

Line IDs `sNN` are in `script.json`; times are in `cues.json`.

## Revision 2 (10 Nov 2026 SGT): island look, two new lines

Owner intake answers (cards in the project thread): keep the island look from the ops sample, revise this film, local Kokoro voice, generic public detail (no dates, IDs or logos).
Two lines were added, so later line IDs moved: old s06–s27 are now s07–s28, and old s28–s30 are now s30–s32. The rows below the table header keep the **old** IDs; add one (or two after s27) to find the line in the new `script.json`.

| # | Claim (new in revision 2) | State | Source at the revision | Line |
|---|---|---|---|---|
| R1 | The whole picture as three places: a connected mainland with GitLab, a vault of private AWS storage, and a sealed island where the run happens, with no bridge to the internet | DOCUMENTED, DEMONSTRATED | `docs/validation-host.md` (subnet with no route to the internet), `docs/cloud-operations.md` §"Proof that the host is cut off" (SSM probe: public sites timed out; S3 and ECR answered through VPC endpoints) | s06 |
| R2 | If anything tries to reach the internet during a run, there is nowhere to go; the run stops, the failed stage is named, and the result is FAIL | IMPLEMENTED (shown as ILLUSTRATIVE) | Podman `--network none --pull=never` (`scripts/ops/generate_pipeline_ecr_overrides.sh`); CodePipeline stops at the failing stage and `scripts/operator/e2e.sh` prints `RESULT=FAIL` | s29 |

The on-screen stage strip uses the ten CodePipeline stage names from `infra/ops` (source, verify-source, validate-intake, check-bundle, check-data, check-images, runtime-preflight, offline-execute, validate-results, publish-report): IMPLEMENTED.


| # | Claim (as narrated or shown) | State | Source at the revision | Line |
|---|---|---|---|---|
| 1 | A workflow needs container images, plugins, reference files and input data at run time | DOCUMENTED | `docs/architecture.md`; `offline/run_pipeline_e2e.sh` header (workflow, data, plugin state, image store) | s01–s02 |
| 2 | With no internet, a missing piece stops the analysis | IMPLEMENTED (shown as ILLUSTRATIVE) | `scripts/ops/generate_pipeline_ecr_overrides.sh:105` (`--network none --pull=never`): nothing can be fetched at run time | s03 |
| 3 | The example is a germline variant-calling test from nf-core Sarek on a small public test dataset | IMPLEMENTED | `offline/pipelines.tsv` row `sarek-310-germline-strelka`: nf-core/sarek 3.10.0, nf-core test-datasets, "Sarek 3.10.0 germline quick demo (Strelka)" | s05 |
| 4 | GitLab is the single trusted home for the solution | OWNER DIRECTION, DOCUMENTED | Issue #765 "Repository roles"; `docs/architecture.md` (protected GitLab main) | s06 |
| 5 | Workflow code lives in a GitLab repository | DOCUMENTED | `docs/architecture.md`; `.gitlab-ci.yml` | s07 |
| 6 | Container images live in the GitLab container registry | OWNER DIRECTION, DOCUMENTED | `docs/architecture.md:50` ("Private GitLab Container Registry"); `.gitlab-ci.yml:176` (scans every image in the project registry). `docs/ops-field-guide.html:248` lists the registry as the images' first stop as not yet tested | s07 |
| 7 | Reference data and test datasets are hosted in GitLab | OWNER DIRECTION, DOCUMENTED | `docs/ops-field-guide.html:293` (R2: code and test data in the GitLab package registry) | s08 |
| 8 | Content is scanned for security; the operations team reviews the findings | IMPLEMENTED (scan), OWNER DIRECTION (review, "as it arrives") | `.gitlab-ci.yml:11–16, 176–192` (Trivy over every registry image; scans report, never block preparation) | s09 |
| 9 | A GitLab Runner prepares the release | IMPLEMENTED | `.gitlab-ci.yml:91` `prepare:sarek-310-germline-strelka` (OIDC `id_tokens`) | s10 |
| 10 | Workflow code goes to AWS CodeCommit | OWNER DIRECTION, DOCUMENTED | `infra/promotion/main.tf:52` (CodeCommit endpoint); `docs/cloud-operations.md` | s10 |
| 11 | Each image goes to private Amazon ECR, locked to its exact identity | IMPLEMENTED | `scripts/operator/e2e.sh:71–94` (every ECR image digest checked against the published manifest) | s11 |
| 12 | Workflow, plugins, references and data go into one S3 bundle with a fingerprint per file | IMPLEMENTED | `offline/run_pipeline_e2e.sh:43` (pre-relocation checksum inventory); `scripts/operator/e2e.sh:82–83` (archive SHA-256) | s12 |
| 13 | Every file and image is read back and compared before the release is registered | IMPLEMENTED | `scripts/operator/e2e.sh:4, 72–94` (one readback, then register); `:39, 104` (`prepared_releases.tsv`) | s14–s15 |
| 14 | A mismatch stops the release | IMPLEMENTED (rejection shown as ILLUSTRATIVE) | `scripts/operator/e2e.sh:83, 92` (`die` on archive or digest mismatch) | s16 |
| 15 | An approved run request in GitLab starts a run with its own unique identity | OWNER DIRECTION (GitLab start), IMPLEMENTED (unique identity) | `ops/requests/README.md:53` (a reused `run_id` is rejected). At the revision the run pipeline's source is the development repository (`infra/ops/main.tf:97–112`) | s17 |
| 16 | CodePipeline runs ten gated stages: source, release, data, images and runtime checks, then execution, result validation and the report | IMPLEMENTED | `infra/ops/main.tf:46–54, 97` (stages 01–10) | s18 |
| 17 | CodeBuild does each stage's work; Systems Manager sends commands to a private EC2 host | IMPLEMENTED | `infra/ops/main.tf:120–140` (one CodeBuild action per stage); `scripts/automation/codepipeline_ops_stage.sh` | s19 |
| 18 | The host has no internet route | DEMONSTRATED | `docs/cloud-operations.md:108` (probe: public sites unreachable, S3 and ECR reachable; route table has no NAT, internet gateway or public IP) | s19 |
| 19 | Private endpoints connect it only to the AWS services it needs | DOCUMENTED | `docs/cloud-operations.md:108` (S3 and ECR through VPC endpoints) | s20 |
| 20 | On the host the bundle is checked again against its fingerprints | IMPLEMENTED | `offline/run_pipeline_e2e.sh:131–151` (relocate, then validate the pre-relocation checksums) | s21 |
| 21 | The exact images are loaded into an isolated container store | IMPLEMENTED | `offline/run_pipeline_e2e.sh:6, 185–199` (isolated Podman store) | s21 |
| 22 | Nextflow runs offline; plugin downloads off; tasks have no network; no image can be pulled | IMPLEMENTED | `offline/run_pipeline_e2e.sh:339–340` (`NXF_OFFLINE=true`, `NXF_PLUGIN_AUTOINSTALL=false`); `scripts/ops/generate_pipeline_ecr_overrides.sh:105` | s22–s24 |
| 23 | The pipeline confirms success, the offline controls and the expected outputs | IMPLEMENTED | `scripts/automation/codepipeline_ops_stage.sh:279–292` (result PASS, no public runtime dependency, offline true, expected outputs PASS) | s25–s26 |
| 24 | A clear PASS or FAIL with an evidence report for the team | IMPLEMENTED | `codepipeline_ops_stage.sh:296–338, 365` (static HTML evidence dashboard, `RESULT=PASS`) | s27 |
| 25 | Tested end to end | DEMONSTRATED | `docs/cloud-operations.md` §4 (proven Sarek runs) | s29 |
| 26 | Repeatable for every release | DOCUMENTED | Every lane uses the same prepare → readback → pipeline path (`.gitlab-ci.yml`, `infra/ops/main.tf`) | s29 |
| 27 | The missing-piece opening and the rejected release | ILLUSTRATIVE | Tagged *Illustration* on screen | s01–s04, s16 |

**Owner-direction rows (4, 6, 7, 8, 10, 15).** The owner describes these as the working solution. At this revision the source documents them as design or partial implementation: GitLab registries are documented, GitLab scanning is implemented as report-only, and CodeCommit appears in the promotion path. Today the run pipeline starts from the development repository. The film states them as working because the owner directed it.

**Deliberately not said:**
- that the controls are a physical air gap
- clinical or scientific validity of variant calls
- promotion to other accounts or production readiness
- any human approval gate
- how long anything takes, or any date
