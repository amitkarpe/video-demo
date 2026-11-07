# Environment

Status: NOT_READY

Record project-specific runtime and dependency truth here. Keep machine-specific facts in the active `~/.config/agent/HOST.md` profile when available instead of duplicating host configuration in every repository.

## Runtime

- Primary host/profile: `~/.config/agent/HOST.md` when available
- Working directory: `<repo path>`
- Runtime: `<local | Codex Cloud | container | hosted app | mixed>`

## Development Tools

List only tools this project actually depends on, for example:

- Python: `<version / not required>`
- Node.js / npm: `<version / not required>`
- Docker/Podman: `<required / not required>`
- Terraform/Terragrunt: `<required / not required>`
- Nextflow: `<required / not required>`

## Optional Codex Cloud Development Setup

See [the repository-owned setup contract](docs/CLOUD_SETUP.md). Fill this section **in a derived project only after selecting its intended development workflow and obtaining the required intent acceptance**. The source template stays unconfigured and does not install software.

- **Setup state:** `UNCONFIGURED` (template default; **not** the same as a deliberately configured `NO_EXTRA_TOOLS` workflow).
- **Required workflow/profile:** `<accepted project workflow or not selected>`; optional profiles are not inferred from repository names or hosting targets.
- **Intended repository / selected managed environment:** `<exact owner/repo and confirmed environment selection>`; mounted checkout and task ref/SHA: `<verified at task time>`.
- **Required tools/versions and services/ports:** specify under **Development Tools** and **External Dependencies**; point to authoritative manifests/lockfiles rather than duplicate version pins.
- **Configuration and network:** `<required variable names, secret/non-secret classification, permitted endpoints; never values>`.
- **Install / activation / service startup:** `<actual repo command(s) or explicitly no installation>`.
- **Readiness and functional check:** `<actual repo command(s), expected result and required failure behavior>`.
- **Optional capabilities:** `<explicit opt-in features; otherwise NOT_RUN>`.
- **Evidence:** `<task revision, selected profile, tool/readiness results; cloud publication and fresh-task proof tracked separately>`.

An intentionally dependency-free project can become ready **only after its selected functional check passes**. The template's `Status: NOT_READY` is unchanged; a setup script or CLI version alone does not imply AWS/cloud authentication or deployment permission.

## Cloud

- Provider: `<AWS / none / other>`
- AWS profile: `<profile or N/A>`
- Region: `<region or N/A>`
- Account/environment alias: `<personal lab / dev / nonprod / prod / N/A>`

Never infer execution authority from an AWS profile name. Authority comes from `SPEC.md` and the active Issue/instruction.

## Optional Provider Execution Identity

For a derived project **only**, record the selected execution route when provider access is actually needed. These are descriptive fields, not credentials, grants or a new runtime gate.

- **Execution plane:** `SOFTWARE_ONLY | GITHUB_OIDC | CODEBUILD_SERVICE_ROLE | DIRECT_CODEX_CLOUD` (choose one in the derived project's approved scope; source template is unconfigured).
- **Provider identity required:** `NO | YES` (software-only workflows need no provider authentication).
- **Target reference:** `<approved private account/role record or NONE>`; reuse the provider/region selectors above.
- **Allowed operations reference:** `<approved SPEC/Issue or NONE>`.
- **Identity status:** `NOT_REQUIRED | NOT_CONFIGURED | READY_VERIFIED | EXPIRED | ACCESS_DENIED | WRONG_ACCOUNT | UNVERIFIED`.
- **Evidence reference:** `<sanitized receipt scoped to target, role, repository, execution plane and session, or NONE>`.

`NOT_REQUIRED` means **no provider identity is needed**, not that installation, functional checks, cloud setup or task execution passed. `READY_VERIFIED` is time- and scope-bound evidence, **not permission** to perform a new operation. Reverify identity and intended service capability when starting authorized provider work; action authority remains in the owning SPEC/Issue. Software-only tasks must not perform identity or permission probes.


## External Dependencies

- `<service, MCP, model platform, database, API, or N/A>`

## Optional Cloud-First App

After project intent is accepted, use the [quickstart](docs/CLOUD_FIRST_QUICKSTART.md).
Choosing a provider is opt-in; this template has no cloud runtime or provisioning default.
Record only the fields needed by the selected app:

- App slug / exact repository / Worker or hosting app name: `<values>`
- Provider account alias / environment / visibility / cost limit: `<values>`
- Production branch / deploy root / command: `<main / root / provider command>`
- Approved custom hostname / DNS configuration owner: `<values or N/A>`
- Non-production preview policy / command / URL visibility: `<disabled or approved>`
- GitHub App repository grant / owner onboarding evidence: `<Issue reference>`
- Build credential scope confirmed by owner/provider: `<evidence reference; no value>`

For Cloudflare, follow [owner onboarding](docs/CLOUDFLARE_WORKERS_ONBOARDING.md).
`<app-name>.amitk.life` is this owner's optional production convention, not a universal
zone or account. Domain, Worker creation and credential changes require explicit scope.
Use the [release receipt](docs/DEPLOYMENT_EVIDENCE.md) for runtime proof; keep `ENV.md`
current-only and preserve generic `NOT_READY` until the new project's readiness is known.

## Credentials And Secrets

Use approved local, cloud, or secret-management mechanisms. Never commit credentials, tokens, private keys, or raw secrets.

## Readiness

Set `Status` to `READY` only when the dependencies needed for the current milestone are known and usable. Use `PARTIAL` when missing dependencies do not block the approved work.
