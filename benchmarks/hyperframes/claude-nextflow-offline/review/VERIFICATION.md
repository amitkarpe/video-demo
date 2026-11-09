# Verification and QA record — "Nextflow Offline: Prepare Once, Run with Confidence"

**VERIFIED** = measured here on the final file. **NOT_VERIFIED / NOT_ASSESSED** = not done or not possible here. A mechanical pass is not owner acceptance.

## 1. Identity
- **Output:** `amitkarpe/video-demo` (public), branch `feat/nextflow-offline-film` from `origin/feat/10-engineering-deep-dive` = `995e828`. Dedicated worktree, folder `benchmarks/hyperframes/claude-nextflow-offline/`. No earlier film or branch was modified.
- **Source:** `amitkarpe/nextflow-offline` (private) @ `356ed30f322a109788ca68f352961a33a7bba046`.
  - Read from a scratch clone with the push URL disabled.
  - No source writes, pipeline runs, cloud operations, scans or worker dispatch.
- **Brief:** Issue #765 in that repository, its two review comments, and the owner's chat direction of 9 Nov 2026:
  - Sarek as the example
  - GitLab as the only repository service, hosting code, container images and datasets, with report-only scanning reviewed by Ops
  - CodeCommit, ECR and S3 as preparation targets
  - one confident working flow, without "proposed" labels, dates, IDs, code or scripts
  - the film placed in `video-demo`
  - unlimited budget
  - sample first or straight to the full film at Claude's discretion
- **Agent:** `claude-opus-5-5` (Opus 5.5), the Claude Code desktop session that also made the Issue #28 film. Effort/reasoning setting: **UNAVAILABLE** (not exposed in-session).
- **Playbook:** `docs/CLAUDE_VIDEO_PLAYBOOK.md` on `main` (merged in PR #29).

## 2. Final file (VERIFIED)

| Check | Artifact | Method | Observed | Disposition |
|---|---|---|---|---|
| Container/codec | `out/claude-nextflow-offline.mp4` sha256 `4bc740294c9a5e41cf9db7fbfb688824deee40b81da5173bdac7f4a1416c9a3c` | `ffprobe` | H.264 High 1920×1080 30 fps yuv420p; AAC-LC 48 kHz stereo; 212.351 s; 80,894,073 bytes | PASS (< 100 MB GitHub limit) |
| Full decode | same | `ffmpeg -v error -i … -f null -` | exit 0, no errors | PASS |
| Full-duration playback | same (the browser fetched the file and hashed it in-page: identical sha256) | Built-in Chromium browser `<video>`, unmuted, `playbackRate` 4 | `played` = [[0, 212.351]], `ended=true`, `error=null`, no error or stall events, 58.9 s wall | PASS at 4× speed. Not a 1× human viewing |
| Motion | same | `mpdecimate` distinct frames | 4,194 of ≈ 6,371 frames distinct | PASS. Every line has a state change or camera move; lint reports no dead stretch |
| Loudness | same | `ebur128=peak=true` | −16.0 LUFS integrated, LRA 2.7 LU, true peak −1.4 dBTP | PASS (house −16 LUFS, ≤ −1 dBTP) |
| Lint | `index.html` | `npx hyperframes check` | 0 errors. Warnings: secondary text below the 28 px *phone* floor (service-tile kickers, stage numbers, rail labels), five identical container sprites, file length | Accepted. The target is a laptop at 720p; essential statements are ≥ 30 px or captioned |
| Captions | `captions.srt` | parsed | 48 cues, ≤ 84 chars (≤ 2 lines at 38 px), min dwell 1.34 s, 0 overlaps, timed from post-edit clip lengths | PASS |
| 720p readability | `review/qa/*.jpg` (22 frames from the final file, including two wipe transitions) | viewed at 1280×720 by Claude, plus the vision QA below | Captions ≈ 25 px at 720p; headlines 30–90 px | PASS for essential text |
| Keyframes | `keyframes/0[1-8]-*.png` | taken from the final file | missing piece · GitLab home · one release · registered · architecture · offline run · PASS · confidence | — |

## 3. Owner direction and the sample gate
- **Sample:** the owner left the choice to Claude. No separate owner-approval sample was made. A 50 s moving slice of the hardest middle section (verify → gated run → architecture map → sealed host) was rendered and reviewed first as a self-check. Two full drafts followed.
- **Defects found and fixed before QA:**
  - the architecture map sat high and left the lower half empty
  - map arrowheads appeared before their lines
  - the registered stamp stayed bright during the illustrated rejection
  - the cold-open pieces became too small while travelling
  - the journey rail was hard to read over the warm workshop
  - "finding" markers overlapped labels
  - the "one release" banner covered the case
  - the evidence panel sat too high
  - static stretches (now slow camera drifts)
  - an alcove label was clipped during a pan
- **Language rule:** the film shows no code, scripts, file names, IDs, hashes or dates, and names no repository service other than GitLab. The only tag is *Illustration*, on the missing-piece opening and the rejected release.

## 4. OpenAI QA (advice, with dispositions)

**Transcription of the final mix** (`gpt-transcribe`, `review/qa-transcribe.json`): WER **0.44%** (2/459). The only difference is an inserted "it can", with no missing or substituted words. Every product name was heard correctly: GitLab, Nextflow, nf-core Sarek, CodeCommit, ECR, S3, CodePipeline, CodeBuild, Systems Manager and EC2. The three provider transcripts flagged as "mismatch" (s05, s17, s20) only spelled out the pronunciation hints ("GIT-lab", "A-W-S"). The independent transcription heard the words correctly. The audio of the final file is unchanged since this pass: `assets/mix.wav` sha256 `b596caf6…f335` was identical before and after the last picture-only fixes.

**Vision review** (`gpt-5.5`, 22 frames of the prior candidate, timestamps and line IDs in the file names, `review/qa-vision.json`): 14 findings.

| Finding (severity) | Disposition |
|---|---|
| Faded "REGISTERED" stamp visible during the fingerprint-mismatch illustration (high, 2 frames) | **Accepted.** The case and stamp now fade out completely before the rejection appears |
| "finding" text markers are extra tags and too small (high/low, 2 frames) | **Accepted.** Replaced with small amber markers with no lettering |
| "✓ SCANNED" pills read as status badges (high, 2 frames) | **Rejected.** They show the narrated scan result on each alcove, not a status hedge. The owner's rule bans "proposed" and status labels about maturity |
| "nf-core/sarek" reads like a repository path (medium) | **Accepted:** "nf-core Sarek", matching the narration |
| Ten stage boxes crowded and small (medium) | **Accepted in part.** Labels 21 → 23 px, numbers brighter, boxes taller. Ten stages stay in one row: it is the narrated structure |
| "FAIL" option too low-contrast (medium) | **Accepted.** Inactive FAIL raised to a readable grey; PASS stays highlighted |
| "Stopped" message low-contrast (medium) | **Rejected.** That frame was taken 0.04 s into its fade-in; the settled message is solid on an opaque pill |
| Sealed-room boundary near the frame edge (low) | **Accepted.** Inset by 40 px |
| Closing timeline labels over bright sky (low, 2 frames) | **Accepted.** Shadows and brighter sub-labels added; positions kept |

Fixes were verified on the next render (frames `review/qa/t0036.5…`, `t0059.0…`, `t0106.5…`, `t0124.0…`, `t0161.5…`, `t0184.5…`). Decode, playback, loudness and motion were re-run on the final hash.

## 5. Narration and sound — **AUDIBLE_REVIEW=NOT_VERIFIED**
- Claude cannot hear. No human has listened to the final mix.
- Machine evidence:
  - the independent final-mix transcription above
  - loudness and true peak measured
  - all 30 takes returned complete audio
- Please listen for:
  - warmth and pace (≈ 148 words per minute)
  - pronunciation of Nextflow, nf-core, Sarek, GitLab, ECR, S3, EC2
  - whether the synthesized score and effects (ducked under the voice) ever compete with speech
- Listening checklist: playbook §8.2.

## 6. Comprehension (self-check, not an audience test)
- **What happened?** One Sarek release was hosted and scanned in GitLab, then prepared into CodeCommit, ECR and S3. It was verified by readback, run through ten gated stages on a private host with no internet route, and accepted on evidence.
- **Why does it work?** Everything is prepared and fingerprinted first. The runtime can use only what was prepared: offline mode, no network, no image pulls. The result is checked rather than assumed.
- **What is limited?** The film is deliberately confident and generic, by owner direction. The owner-direction claims are marked in `CLAIMS.md`. There are no on-screen caveats beyond the two *Illustration* tags.

No viewer study was done.

## 7. Spend (OpenAI, this film; settled from returned usage at published rates, estimates)

| Endpoint · model | Requests | USD |
|---|---:|---:|
| `images/generations` · `gpt-image-2.6-sunburst` (high) | 9 | 0.4004 |
| `images/edits` · `gpt-image-2.6-sunburst` (open case from the closed case) | 1 | 0.0547 |
| Realtime `wss` · `gpt-realtime-2.1`, voice `marin` (30 lines, no re-takes) | 30 | 0.3194 |
| `audio/transcriptions` · `gpt-transcribe` (final-mix QA) | 1 | 0.0160 |
| `responses` · `gpt-5.5` (vision QA, 22 frames) | 1 | 0.2418 |
| **Total committed** | **42** | **1.0323** |

- Budget: unlimited by owner direction. The ledger used a working cap of USD 50 (stop at 45) so it remained a real stop.
- All 42 requests ACK. No retries, no uncertain or unsettled reservation.
- The owner's OpenAI dashboard is authoritative.
- Model visibility lookups (HTTP 200) were non-generating.
- No Sora, video generation or live-voice app. No AWS or other paid service. The key came from the owner-allowed, gitignored env file and was never printed or committed.

## 8. Usage and time
- **Start:** 2026-11-09 ≈ 17:38 SGT (worktree and preflight). **Final file verified:** 2026-11-09 18:16 SGT (≈ 38 min, plus documentation and delivery).
- **Revisions:**
  - images: 10 (9 generations + 1 edit), 0 regenerated
  - narration: 30 takes, 0 re-takes
  - script: 1 version (the owner-reviewed text, unchanged in meaning)
  - renders: 1 slice, 1 full draft, 3 delivery renders (+ web encodes)
  - QA: 1 final-mix transcription, 1 vision pass
- **Agent tokens: UNAVAILABLE as per-model counters.** The in-session tools expose no input/output/cache counters. Observable proxies:
  - context window 366k of 1M tokens at delivery. This is occupancy, not consumption, and the session also spans the Issue #765 review.
  - Pro plan 5-hour window at 6% and weekly at 5% after production. No reading was taken at the start of this film.
- No agent inference cost is visible on a subscription.

## 9. Rubric self-evaluation (evidence, not a score; owner scores)

| Area (weight) | Evidence | Known weakness |
|---|---|---|
| Technical accuracy and clarity (30) | `CLAIMS.md` (27 claims with states and sources); the vision and transcription findings acted on | Six claims rest on owner direction rather than the source revision; the stage names are paraphrased |
| Visual art direction (25) | Ten AI plates and sprites in one world; the same release case in every scene, with the open case as a reference edit | The architecture map is a diagram over a dimmed plate |
| Motion, camera, continuity (20) | Case travel and rewind, alcove tour, scan sweep, three lanes, inspection scan, ten-arch bridge, map build, pods, journey rail | Eased 2D camera moves, not 3D |
| Narration, pacing, sound (15) | Verbatim Realtime voice; 0.44% WER; −16 LUFS | **Not audibly reviewed** |
| Readability and subtitles (10) | 720p frames; captions ≥ 1.34 s, ≤ 84 chars | Tile kickers and stage numbers are small (secondary) |

Total: NOT_ASSESSED (no /100 without human viewing and listening).
