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
- Shared scripts: `toolkit/`. `ssm-patch` and `cis-hardening` build byte-identically through it; `offline-validation` revision 2 (island look, Kokoro voice) has its own `build.py`. Older films keep their own frozen scripts.

## Active Work
- No open PRs. Consolidation (#40) is merged; the earlier film PRs are closed as superseded, and their branches are kept.
- Owner reviews pending: `cis-hardening`, `offline-validation`, `claude-film` (human listening not yet done).

## Next Action
- Next film request: run `docs/VIDEO_INTAKE.md`, reuse a house look, start with `toolkit/new_film.py`.

## Restart
Begin with `AGENTS.md`, then the active Issue/PR. For a film request, read `docs/VIDEO_INTAKE.md` and `docs/STYLE_CATALOG.md` first.
