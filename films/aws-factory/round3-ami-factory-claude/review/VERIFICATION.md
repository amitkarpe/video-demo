# Verification — Round 3, Claude lane ("BlueOps: the AMI Factory")

**VERIFIED** means measured here. **NOT_VERIFIED** means not done or not possible here. A mechanical pass is not owner acceptance.

## 1. Identity and revision
- Repo `amitkarpe/video-demo` (public). New branch `feat/round3-claude-blueops-ami`, created from `995e8287847b77f81707e485f9767700bc98c162`; that commit equals `origin/feat/10-engineering-deep-dive` (verified at start). The pilot commit is the PR head.
- Worktree `/Users/apple/git/worktree/video-demo-23-claude-blueops-ami`. No other branch or writer was using this name. PRs #21/#22, earlier rounds and the competitor's worktree were not read or written.
- Model that actually ran: **`claude-opus-5-5`** (Claude Code desktop, the existing session; the owner switched to it with `/model`). Reasoning/effort setting: **UNAVAILABLE**, because it is not exposed inside the session.
- Technical source, read-only: `amitkarpe/ami-factory` @ `2cfd64667a93b8183f574da30f86c39af7089dcb`. Files read:
  - README
  - SPEC.md
  - `docs/current/AMI_FACTORY_DIRECTION.md`
  - `docs/current/VALIDATION_CONTRACTS.md`
  - `docs/current/E2E_DEV_TO_PROD_VALIDATION.md`
  - `docs/current/SHARED_PIPELINE_LIFECYCLE_CONTRACT.md`
  - `docs/current/AMI_FACTORY_V3_LIFECYCLE_CONTRACT.md`
  - `docs/current/MONGODB_83_PROD_READINESS_STATUS.md`
  - a keyword scan of the ops/automation plans

## 2. Claims vs. source (paraphrased; no private text, IDs or code reproduced)

| Film claim | Status shown | Basis |
|---|---|---|
| Lineage: GCC Golden AL2023 → Hardened Base OS → GitLab / MongoDB / CloudOS ECS Worker; GitLab + Nextflow optional; no container-runtime middle parent | CURRENT | README and SPEC "Product Family Contract"; DIRECTION "Canonical Lineage" |
| Hardened Base OS = golden image + package-only GCC agents (no manager registration baked) + a selected CIS profile, not full compliance | CURRENT | SPEC "Final Hardened Base OS contract"; README "Base Contract"; DIRECTION |
| Base checks: private instance, no public IP, SSM online, expected packages, recorded profile | CURRENT | VALIDATION_CONTRACTS "Shared Gates" and "Hardened Base OS" |
| Hardened Base OS is a DEV-only parent, never shipped to PROD | CURRENT | SPEC architecture invariants |
| GitLab carries its own container runtime; MongoDB has no containers; ECS Worker adds the container engine and ECS agent | CURRENT | DIRECTION "Child Contracts" |
| GitLab gates: healthy, clone/push, create/read data, persistence across reboot | CURRENT | VALIDATION_CONTRACTS "GitLab" required gates and runtime gates |
| MongoDB gates: private listen only, ping, CRUD, dump/restore | CURRENT | VALIDATION_CONTRACTS "MongoDB" |
| A single-node smoke test does not prove a cluster; replica-set gate | PROPOSED | VALIDATION_CONTRACTS ("basic standalone smoke does not prove replica-set readiness"); owner brief |
| ECS: task placement on the exact candidate; 0 placed = failure | CURRENT | VALIDATION_CONTRACTS "CloudOS ECS Worker" |
| ECS mock services and ports; scoped parameter reads via IAM | PROPOSED | Owner brief (not in current contracts) |
| Lineage, encrypted and shareable snapshot, private launch | CURRENT | VALIDATION_CONTRACTS shared gates; DIRECTION "Shareable KMS Rule" |
| A fail or an unknown stops the line; build success ≠ promotion | CURRENT | VALIDATION_CONTRACTS ("do not claim PASS unless evidence exists"); SHARED_PIPELINE_LIFECYCLE ("build success is not promotion") |
| EventBridge-style discovery signal | PROPOSED | Owner brief; no EventBridge found in the repo scan |
| Phase A: share to PROD, private launch, re-check with PROD's own configuration, manual approval, pointer moves, previous release kept for rollback | CURRENT model (human-approved) | E2E_DEV_TO_PROD; SPEC "PROD promotion" and "SSM responsibilities"; SHARED_PIPELINE_LIFECYCLE (Manual Approval; previous/rollback pointer); V3 lifecycle (current/previous pointers) |
| Phase B: weekly candidates, first-Saturday-night scheduled promotion only after a management/security/change-governance approved policy; blockers; urgent Ops-approved path; canary rollback within an agreed window | PROPOSED (persistent chip) | Owner brief only. The film says "not today's system" in voice and picture |

Deliberately **not** claimed: unattended monthly PROD rollout today; full CIS compliance; zero vulnerabilities; scan/HCR acceptance; that DEV validation alone is enough for PROD; any real account, VPC, subnet, AMI, pointer or KMS identifier.

## 3. File, decode, playback (VERIFIED)
- **Final film:** `out/round3-claude-blueops-ami.mp4`, 60,199,574 bytes, SHA-256 `89f7551fdc118a0a7cad800295df4b1e503af012b33f11209263860bf5809a95`.
  - H.264 High, yuv420p, **1920×1080**, 30 fps, 236.300 s, 7,089 frames; AAC LC 48 kHz stereo.
  - It is a CRF 20 web encode of the HyperFrames delivery render, which is ≈ 156 MB and gitignored because GitHub caps files at 100 MB.
- **Preview:** `out/round3-claude-blueops-ami-preview.mp4`, 1,726,720 bytes, 960×540, 30 s, SHA-256 `2f2f4666f1aaf4c6c7a6dc77755d0307f03e006623fe6b51082542800ba4853f`.
- **Full decode:** `ffmpeg -v error -i <file> -f null -` exits 0 with no errors for both files.
- **Changing frames:** `mpdecimate` keeps 4,213 of 7,089 frames as distinct. A per-line contact sheet (one frame per narration line) shows the picture changing on every line.
- **Loudness** (`ebur128`): integrated −17.8 LUFS, LRA 3.0 LU, true peak −1.1 dBFS.
- **QuickTime Player:** opened the final file with a duration of 236.3 s and advanced during playback (0 → 2.67 s).
- **`npx hyperframes check`:** 0 errors. Remaining warnings:
  - file size
  - a duplicate image source (the same machine sprite is used in two scenes)
  - one contrast note on deliberately dim "unticked" ghost check glyphs
  - type-floor notes on secondary labels
- **Camera:** clamped in code so the generated plates always cover the frame (fixed a plate-edge strip found in review).

## 4. 720p readability (VERIFIED by viewing)
`review/qa/*.jpg` are scaled to 1280×720.
- Captions: 38 px at 1080p, ≈ 25 px at 720p, on a dark box.
- Panel rows: 26 px.
- Chips: ≥ 20 px.
- Payoff type: 108 px.
- Every essential statement is spoken, captioned and shown in large type or a chip.

## 5. OpenAI QA (used as tools, not as acceptance)
| Pass | Model | Result | What changed |
|---|---|---|---|
| Vision, draft 2 (15 frames) | `gpt-5.5` (Responses, image input) | 15 findings | Title now names GCC and Amazon Linux 2023; "snapshot or KMS key access"; DEV panels no longer clip; larger and brighter upstream/Phase A/B text; stamp moved |
| Vision, final candidate (10 frames) | `gpt-5.5` | 11 findings | BLOCKED stamp no longer covers the list; "future monthly auto-promotion"; "missing governance or release approval"; inactive panels less dim; end chip says PROPOSED |
| Kept by owner-brief decision | — | — | "Ops-approved" urgent release and upstream "baseline hardening, some agents" are the brief's own words. The reviewer was given only a condensed rule list |
| Transcription, draft 2 and final | `gpt-transcribe` | WER 1.55% → 1.35% (7 of 517 words) | Differences are spelling splits ("Event Bridge", "Cloud OS"), one article, and "through scoped IAM" heard as "they're scoped IAM" in s23 |

The s23 finding is worth a human listen. The Realtime transcript for that take matched the script exactly.

## 6. Spend (OpenAI, this lane; settled from returned usage)

| Endpoint / model | Requests | USD |
|---|---:|---:|
| `images/generations` · `gpt-image-2.6-sunburst` (high) | 6 | 0.2577 |
| `images/edits` · `gpt-image-2.6-sunburst` | 1 | 0.0617 |
| Realtime `wss` · `gpt-realtime-2.1`, voice `marin` (40 lines, all verbatim) | 40 | 0.3705 |
| `responses` · `gpt-5.5` (vision QA) | 2 | 0.3612 |
| `audio/transcriptions` · `gpt-transcribe` (QA) | 2 | 0.0355 |
| **Total committed** | **51** | **1.0867** |

- Cap USD 10.00, so **USD 8.91 remains**. All 51 requests returned ACK; there were no retries and no uncertain charges.
- Costs are computed from each response's `usage` at the published rates, so they are estimates. The owner's dashboard is authoritative.
- No Sora, video generation or GPT-Live. No AWS call, hosting or other paid service. Key never printed or committed.

## 7. Narration and sound — **AUDIBLE_REVIEW=NOT_VERIFIED**
Claude cannot hear audio, and no human has listened to the final mix.
- Machine evidence: the Realtime output transcript matches all 40 lines exactly; `gpt-transcribe` WER is 1.35%.
- The score and SFX levels were measured (true peak −1.1 dBFS, ducking under the voice) but not heard.
- Please listen for: voice warmth and pace; the pronunciation of AMI, GovTech, GCC, CIS, SSM, MongoDB, Nextflow and EventBridge; "through scoped IAM"; and music/SFX balance.

## 8. Effort, time, tokens
- **STARTED_AT_SGT** 2026-11-08 17:57; the **FINISHED_AT_SGT** time and elapsed minutes are in the Issue #23 result comment.
- Provider input/output/cached/reasoning tokens for the agent: **UNAVAILABLE**. The Claude Code app exposes only context-window size (one session shared with Rounds 1–2) and plan-percent use on a Pro subscription.
- Agent inference cost: **UNAVAILABLE**. A subscription has no per-token bill visible to the agent.
- **Revisions:**
  - research: one pass over 9 source docs plus OpenAI docs/pricing
  - images: 7 generations, 0 rejected
  - script: 1 version (40 lines)
  - narration: 1 Realtime pass (40/40 verbatim) plus pause tightening
  - renders: 2 standard drafts and 4 delivery renders
  - QA: 2 vision passes and 2 transcription passes, with 4 fix rounds

## 9. Self-evaluation against the rubric (evidence, not a score)
| Criterion | Evidence | Known weakness |
|---|---|---|
| Technical accuracy (30) | §2 table; CURRENT/PROPOSED grammar on every frame; no private data | Simplified to one candidate per family; pointer and evidence storage only implied |
| Visual beauty (25) | Keyframes; seven consistent AI plates/sprites; the edit-based golden → hardened continuity | Phase B relies on cards over one plate |
| Motion and continuity (20) | Forge dive, flash and morph; core → three branches; light-wipe transitions; scan beams; pointer move | Camera moves are eased tweens, not physical 3D |
| Narration and sound (15) | Verbatim Realtime voice; chapter-following score; event-tied SFX | **Not audibly reviewed** |
| Readability (10) | §4 720p frames; both vision passes acted on | DEV overview panels are dense |

Final judgement is Amit's side-by-side viewing.
