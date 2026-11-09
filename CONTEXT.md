# Context

Status: INITIALIZED

> Current-only recovery state. History lives in Git, closed Issues/PRs and the film folders' records.

## Project Identity
- Project: Video Demo (technical explainer films)
- Primary repository: `amitkarpe/video-demo` (public)
- Source repositories the films explain (read-only): `amitkarpe/aws-factory`, `amitkarpe/awsops`, `amitkarpe/nextflow-offline`, `kcloud1/agentic-pentest-poc`
- Owner: Amit Karpe

## Current Truth
- All films live under `films/<source-repo>/<film>/`. Their MP4s are on GitHub Releases tagged `film-<source-repo>-<film>`.
- Default look: `toy-world-3d` (accepted SSM Patch Manager film). Reuse first; no new theme unless Amit asks for one.
- Every new film starts with `docs/VIDEO_INTAKE.md`, then a storyboard-only Phase 1 when reusing a house look.
- Default OpenAI cap: USD 5 per film. The ledger stops at 90% of the cap.
- Shared scripts: `toolkit/`. The three newest films (`ssm-patch`, `cis-hardening`, `offline-validation`) build byte-identically through it. Older films keep their own frozen scripts.

## Active Work
- The consolidation PR brings every earlier branch's work to `main`. After it merges, the old stacked PRs are closed as superseded; their branches are kept.
- Owner reviews pending: `cis-hardening`, `offline-validation`, `claude-film` (human listening not yet done).

## Next Action
- Owner: merge the consolidation PR.
- Agent: close the superseded PRs, then use the intake card for the next film.

## Restart
Begin with `AGENTS.md`, then the active Issue/PR. For a film request, read `docs/VIDEO_INTAKE.md` and `docs/STYLE_CATALOG.md` first.
