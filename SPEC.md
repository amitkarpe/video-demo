# Specification

Status: ACTIVE
Context: PERSONAL (public portfolio of explainers about Amit's work)
Environment: LOCAL macOS (Apple Silicon) plus public GitHub

## Objective
Produce clear, accurate, repeatable technical explainer films, reusing house looks and one shared toolkit, so a new film takes hours, not days.

## Outcome
For each film: an MP4 on a GitHub Release, and in `films/<source-repo>/<film>/` the captions, transcript, keyframes, editable source, evidence map (`CLAIMS.md`), QA record (`review/VERIFICATION.md`) and spend ledger.

## Authorized (standing, for film work in this repository)
- Read the source repositories **read-only**, from scratch clones with the push URL disabled.
- Create branches, worktrees, issues, draft PRs and GitHub Releases in `amitkarpe/video-demo`.
- OpenAI calls for narration, images and QA, up to **USD 5 per film** unless the owner sets another cap.
- Local tools: HyperFrames, Node, Python, FFmpeg and the built-in browser for playback checks.

## MUST
- Start every new film with the [intake card](docs/VIDEO_INTAKE.md). Always confirm the style and the exact names.
- **Reuse first.** Use a house look from `styles/` and the shared `toolkit/`. Create a new theme only when the owner explicitly asks for one.
- Phase 1 (storyboard) before full production, unless the owner says to skip it.
- Run the QA gates of the playbook on the final file. Record AUDIBLE_REVIEW=NOT_VERIFIED until a human listens.
- Public output stays generic: no account or resource IDs, host names, exact times, dates, patch counts or credentials.

## MUST NOT
- Write to source repositories, or run any AWS or cloud operation.
- Merge without the owner's explicit word.
- Commit secrets, `.env` files or MP4 deliverables (they go to Releases).
- Present a real production gap as a fact in a public film.

## Verification
Decode, full-duration 4× browser playback with an in-page hash, motion (`mpdecimate`), 720p frames, captions, −16 LUFS, an independent transcription of the final mix, and a vision review with written dispositions. The pinned download must be byte-identical.

## Stop Gates
A missing source, an unknown or unapproved name, spend above the cap, a public-safety doubt, or a request that needs a new look (confirm it first).

## Acceptance
The owner's explicit verdict on the film, recorded in its QA record and on the owning issue.
