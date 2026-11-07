# Codex Cloud development setup (optional)

This is the **single repository-owned guide** for preparing an approved development workflow in Codex Cloud. It does not choose the project's purpose or authorize cloud access, spending or deployment. [`AGENTS.md`](../AGENTS.md) routes the agent; [`INIT.md`](../INIT.md) owns first-intent acceptance; [`ENV.md`](../ENV.md) owns project-specific requirements; [the cloud-first quickstart](CLOUD_FIRST_QUICKSTART.md) separately covers hosting and release.

The universal `repo-starter` is **UNCONFIGURED**: leave its Codex Cloud **Install script unset**, its `INIT.md` at `NOT_INITIALIZED` and its `ENV.md` at `NOT_READY`. Do not install tools merely because an optional example exists.

## One contract, small adapters

| Location | Owns |
| --- | --- |
| `AGENTS.md` | Conditional read router and repository/intent safety boundaries |
| `INIT.md` | First-project interview and explicit owner acceptance; never invoked by a shell installer |
| `ENV.md` and project manifests/lockfiles | Selected development workflow, actual versions, services, config **names** (not values), endpoints, commands and readiness criteria |
| Existing project commands; optional `scripts/setup.sh` / `scripts/check-env.sh` | Noninteractive locked installation, repeatable activation and required checks **only if that project needs them** |
| Codex Cloud **Install script** | Short wrapper calling the adopted repository setup command after the correct repository/environment is verified |
| Codex Cloud **Start skill** | Agent instructions for binding verification, reading relevant contracts, starting task-owned services and checking readiness |

Do **not** add mandatory placeholder executables to the universal template. Reuse existing `npm ci`, `python`, build/test commands or a real project-owned script when appropriate. Do not create a second `setup.md` or a universal installation framework.

## Admission and repository-binding check

Before saving or executing a project Install script, and before changing repo content:

1. Identify the **intended** exact `owner/repo` and the owning Issue/PR from the task, not from the Git checkout itself.
2. Confirm the **managed Codex Cloud environment's configured repository** (and relevant ref) through supported product settings or runtime metadata. If this identity is unobservable, record `MANAGED_BINDING=UNVERIFIED`; for a task requiring confirmed binding, stop rather than guess.
3. Independently inspect the **mounted checkout**: `git rev-parse --show-toplevel`, `git rev-parse HEAD` and `git status -sb`; inspect the configured Git remote **without printing any credential-bearing URL**. Compare its canonical repository identity to the intended target. HTTPS, SSH and proxy-backed remotes can differ; do not disclose embedded credentials, equate an arbitrary proxy URL with the intended GitHub repo, or accept `origin` as the source of the expected identity.
4. Treat a valid task branch or detached checkout as normal if its SHA/ref matches the intended task. A directory name, accessible GitHub Issue or working Git fetch does **not** prove the managed environment's repository binding.
5. On mismatch: `BLOCKED_REPO_MISMATCH`. Identify the intended target and the one product setting that must be corrected. Do **not** clone, retarget or create another workspace to hide the mismatch.

## Profile and readiness semantics

- **UNCONFIGURED:** the intended workflow is unknown. Install **nothing**; report `NOT_READY`. This is the universal template state.
- **CONFIGURED_NO_EXTRA_TOOLS:** owner deliberately accepted a workflow needing no extra packages. Run its declared representative check; do **not** report PASS just because setup is a no-op.
- **CONFIGURED_PROFILE:** install **only** selected required tools using pinned, integrity-checked sources and existing lockfiles, then run all required version, build/test and functional checks. Missing required tools, configuration or service responses **fail** with actionable diagnostics and nonzero check status. Optional unselected checks are `NOT_RUN`; they cannot compensate for a required failure.

Choose development tools separately from the hosting/build destination. GitHub Pages and Cloudflare Workers do not imply AWS tooling; AWS M6 `core`, `cloudops` and `app-dev` are opt-in from [`cloud-app-factory`](https://github.com/kcloud1/cloud-app-factory/blob/48ab0ffa8d5615822d6ab99c516709c42f1070b1/docs/aws-toolkit.md). Amplify Hosting and CodeBuild require their own selected project workflow and deployment authority; CodeBuild builds artifacts rather than automatically hosting a website. Provider identity, permissions, network reachability and deployment are **separate proofs** from CLI installation.

### Provider identity is a separate, optional decision

When provider access is needed, the derived project's [`ENV.md`](../ENV.md) may record the **execution plane**, whether identity is required, a reference to approved target/role details, the allowed-operations Issue/SPEC and a scoped evidence receipt. Software/tool readiness, provider identity, service capability and **authorization to act** are distinct. A `SOFTWARE_ONLY` project does not authenticate or run provider probes.

For separately approved AWS CI operations, prefer existing reviewed GitHub Actions with narrowly scoped OIDC roles. CodeConnections grants CodeBuild access to GitHub **source**, not AWS caller authority; CodeBuild uses its own service role. Direct Codex Cloud identity remains **unproven** until the selected runtime supports and verifies an appropriate short-lived mechanism. No route silently creates IAM roles, CI workflows, connections or infrastructure. For any later OIDC trust, check the actual issuer, audience, subject and exact repository/environment restrictions against current official documentation.


## Codex Cloud UI examples — adapt after project intent acceptance

**Blank starter:** Leave **Install script** empty. No bootstrap shell command or repository install profile is selected. Its Start skill may guide the agent through the existing `INIT.md` interview, but must not mark the repository READY.

**Install script, for an initialized/adopted project with a real setup command only:**

~~~sh
# EXAMPLE ONLY: replace the checkout path after verifying the product's
# intended managed repository binding and the mounted Git identity.
set -eu
cd /workspace/REPLACE_WITH_PROJECT
test "$(git rev-parse --show-toplevel)" = "$PWD" || {
  echo "BLOCKED_REPO_MISMATCH: checkout root differs" >&2
  exit 1
}
test -f scripts/setup.sh || {
  echo "UNCONFIGURED: adopt a real project setup command first" >&2
  exit 1
}
bash scripts/setup.sh
~~~

Do **not** paste this unchanged: the example is not a managed-environment binding validator, and `scripts/setup.sh` does **not** exist in the source template. A project with no installation need should leave the field empty; if a project already has a tested setup command, call it directly instead of wrapping it merely to match the sample. Installation must be noninteractive, idempotent, pinned/locked, credential-safe and free of provider mutations.

**Start skill, for an existing task in the selected repository:**

~~~text
Use the existing selected managed Codex Cloud environment and checkout.
Identify intended owner/repo from this task + Issue/PR; confirm the product's
repository binding where observable, then compare the mounted Git checkout
and intended SHA/ref. Stop with BLOCKED_REPO_MISMATCH on contradiction.
Read AGENTS.md; follow its cold/warm router rather than rereading all files.
If INIT.md is NOT_INITIALIZED, ask only unresolved material questions in chat
and await explicit owner acceptance before significant project implementation.
The install shell must never interview or accept intent.
For accepted workflows, consult ENV.md and docs/CLOUD_SETUP.md when relevant.
Activate retained toolchains; start only required task-owned local services.
Run the actual required readiness command and representative functional check;
report REQUIRED_PASS, REQUIRED_FAIL, OPTIONAL_NOT_RUN or UNCONFIGURED distinctly.
Do not infer AWS/cloud auth, deploy authority or retained running processes.
Record exact repo, task SHA, profile and evidence in the owning Issue/PR.
~~~

A Start skill field is an **instruction to the agent**, not a shell script or automatically installed `SKILL.md` file.

## Lifecycle and truthful proof

1. **Initialize project:** agent inspects current truth and asks only missing `INIT.md` questions; record the accepted intent. Setup cannot self-accept intent.
2. **Prepare the current machine:** run only the approved profile's project-owned commands. Preserve tracked files/lockfiles, verify integrity and avoid secrets in caches or logs. An install command succeeds only as far as its own checks prove.
3. **Save UI configuration:** copy the tested project-specific Install script/Start skill into the selected Codex Cloud environment. Repository docs do **not** automatically populate these fields.
4. **Publish:** confirm a successful product-side publication; a saved draft is not a published environment.
5. **Start a fresh task:** confirm managed repository binding, restored tool PATH/files, re-established runtime authentication where separately authorized, service startup and a real functional check. Snapshotted files do not imply running processes survive.
6. **Refresh when needed:** re-prepare after pinned versions, lockfiles, runtime/architecture or chosen capabilities change; report cold/warm results without assuming stale caches are safe.

A check report must distinguish `UNCONFIGURED`, `REQUIRED_FAIL`, `OPTIONAL_NOT_RUN`, `INSTALL_PASS`, `FUNCTIONAL_PASS`, `PUBLISHED` and `FRESH_TASK_PASS`. Never claim a service PASS from just an open port/PID, deployment from a dry-run, or provider auth from installed binaries. Stop once the selected, approved acceptance checks pass.

## Examples — patterns, not universal defaults

| Derived repository / role | Example workflow |
| --- | --- |
| `amitkarpe/repo-starter` (source) | Inert template; no install, no readiness claim |
| `kcloud1/cloud-app-factory` (shared tools) | Python standard library for factory work; M6 AWS tool profiles optional |
| `kcloud1/factory-pilot` (Cloudflare demo) | Node 24 and pinned local Wrangler; `npm ci`; GitHub Actions remains sole deployment writer |
| `kcloud1/aws-factory-pilot` (M7 AWS software pilot) | Pinned M6 `core` proved in managed cloud at factory SHA `48ab0ffa8d5615822d6ab99c516709c42f1070b1`; no authenticated AWS API/deployment inferred |

Project-specific contracts and proof belong in the individual project repository/Issue; the table does not create new obligations or authorize cross-repository changes. Track future real setup-script adoption and repeatability under [roadmap #27](https://github.com/amitkarpe/repo-starter/issues/27).
